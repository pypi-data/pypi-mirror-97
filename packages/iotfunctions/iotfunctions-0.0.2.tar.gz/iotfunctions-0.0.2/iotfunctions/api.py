# Licensed Materials - Property of IBM
# 5737-M66, 5900-AAA, 5900-A0N, 5725-S86, 5737-I75
# (C) Copyright IBM Corp. 2020 All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication, or disclosure
# restricted by GSA ADP Schedule Contract with IBM Corp.
import datetime as dt
import gzip
import inspect
import logging
import os
import re
import traceback
import warnings
from collections import defaultdict
from functools import partial
from pathlib import Path

import ibm_db
import numpy as np
import pandas as pd
import pandas.tseries
import pandas.tseries.offsets

from iotfunctions import dbhelper, dbtables, aggregate, loader
from iotfunctions.db import Database
from iotfunctions.metadata import EntityType
from iotfunctions.pipeline import CalcPipeline
from iotfunctions.stages import ProduceAlerts, PersistColumns
from iotfunctions.util import get_fn_expression_args, get_fn_scope_sources, log_data_frame, UNIQUE_EXTENSION_LABEL
from . import cos, util, dblogging
from .catalog import Catalog

COS_BUCKET_KPI = os.environ.get('COS_BUCKET_KPI')
COS_BUCKET_LOGGING = os.environ.get('COS_BUCKET_LOGGING')
if COS_BUCKET_KPI is not None and len(COS_BUCKET_KPI.strip()) == 0:
    COS_BUCKET_KPI = None
if COS_BUCKET_LOGGING is not None and len(COS_BUCKET_LOGGING.strip()) == 0:
    COS_BUCKET_LOGGING = None

DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING')

ICP_ENVIRONMENT_VARIABLE = os.environ.get("isICP")

DATA_ITEM_NAME_KEY = 'name'
DATA_ITEM_TYPE_KEY = 'type'
DATA_ITEM_COLUMN_NAME_KEY = 'columnName'
DATA_ITEM_COLUMN_TYPE_KEY = 'columnType'
DATA_ITEM_TRANSIENT_KEY = 'transient'
DATA_ITEM_SOURCETABLE_KEY = 'sourceTableName'
DATA_ITEM_TAGS_KEY = 'tags'

CATALOG_FUNCTION_NAME_KEY = 'name'
CATALOG_FUNCTION_MODULETARGET_KEY = 'moduleAndTargetName'
CATALOG_FUNCTION_CATEGORY_KEY = 'category'
CATALOG_FUNCTION_DESCRIPTION_KEY = 'description'
CATALOG_FUNCTION_INPUT_KEY = 'input'
CATALOG_FUNCTION_OUTPUT_KEY = 'output'
CATALOG_FUNCTION_TAGS_KEY = 'tags'
CATALOG_FUNCTION_INCUPDATE_KEY = 'incrementalUpdate'

KPI_FUNCTION_NAME_KEY = 'name'
KPI_FUNCTION_FUNCTIONNAME_KEY = 'functionName'
KPI_FUNCTION_FUNCTION_ID_KEY = 'kpiFunctionId'
KPI_FUNCTION_ENABLED_KEY = 'enabled'
KPI_FUNCTION_GRANULARITY_KEY = 'granularity'
KPI_FUNCTION_INPUT_KEY = 'input'
KPI_FUNCTION_OUTPUT_KEY = 'output'
KPI_FUNCTION_SCOPE_KEY = 'scope'
FUNCTION_PARAM_NAME_KEY = 'name'
FUNCTION_PARAM_TYPE_KEY = 'type'
AGGREGATOR_INPUT_SOURCE_KEY = 'source'
AGGREGATOR_OUTPUT_SOURCE_KEY = 'name'

PARQUET_DIRECTORY = 'parquet'

SQL_STATEMENT_ENTITIES_SIZE = 20000
STALE_DEVICE_CRITERIA = 60

KPI_ENTITY_TYPE_ID_COLUMN = 'entity_type_id'
KPI_ENTITY_ID_COLUMN = 'entity_id'

ENGINE_INPUT_REQUEST_TEMPLATE = '/api/kpi/v1/{0}/engineInput/{1}'
GRANULARITY_REQUEST_TEMPLATE = '/api/granularity/v1/{0}/entityType/{1}/granularitySet'
KPI_FUNCTION_REQUEST_TEMPLATE = '/api/kpi/v1/{0}/entityType/{1}/kpiFunction'
GRANULARITY_SETSTATUS_TEMPLATE = '/api/granularity/v1/{0}/entityType/{1}/setPipelineStatus'

# Timestamps and timestamp formats for database queries
SQL_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

# Currently, all event and dimension tables are expected to store the entity ID in column DEVICEID (as VARCHAR)
ENTITY_ID_COLUMN = 'deviceid'
ENTITY_ID_NAME = 'ENTITY_ID'
DATAFRAME_INDEX_ENTITYID = 'id'
DEFAULT_DATAFRAME_INDEX_TIMESTAMP = 'timestamp'

DATA_ITEM_TYPE_DIMENSION = 'DIMENSION'
DATA_ITEM_TYPE_EVENT = 'EVENT'
DATA_ITEM_TYPE_METRIC = 'METRIC'
DATA_ITEM_TYPE_DERIVED_METRIC = 'DERIVED_METRIC'

DATA_ITEM_TAG_ALERT = 'ALERT'
DATA_ITEM_TAG_EVENT = 'EVENT'
DATA_ITEM_TAG_DIMENSION = 'DIMENSION'

DATA_ITEM_DATATYPE_BOOLEAN = 'BOOLEAN'
DATA_ITEM_DATATYPE_NUMBER = 'NUMBER'
DATA_ITEM_DATATYPE_LITERAL = 'LITERAL'
DATA_ITEM_DATATYPE_TIMESTAMP = 'TIMESTAMP'

TYPE_COLUMN_MAP = {DATA_ITEM_DATATYPE_BOOLEAN: 'value_b', DATA_ITEM_DATATYPE_NUMBER: 'value_n',
                   DATA_ITEM_DATATYPE_LITERAL: 'value_s', DATA_ITEM_DATATYPE_TIMESTAMP: 'value_t', }

logger = logging.getLogger(__name__)


class AnalyticsService:
    SUCCESS_MESSAGE = '\n#############################################' \
                      '\n# Execution of KPI pipeline was successful. #' \
                      '\n#############################################'

    SUCCESS_MESSAGE_NOTHING_TO_DO = '\n#################################################################################' \
                                    '\n# Execution of KPI pipeline was successful. There were no KPIs to be processed. #' \
                                    '\n#################################################################################'

    FAILURE_MESSAGE = '\n#########################################' \
                      '\n# Execution of KPI pipeline has failed. #' \
                      '\n#########################################'

    INIT_FAILURE_MESSAGE = '\n##############################################' \
                           '\n# Initialization of KPI pipeline has failed. #' \
                           '\n##############################################'

    def __init__(self, tenant_id, entity_type_id, local_log_file_name, engine_input=None, production_mode=True, log_level=None,
                 dblogging_enabled=True, log_keep_days=90):

        try:
            self.local_log_file_name = local_log_file_name
            self.logger_name = '%s.%s' % (self.__module__, self.__class__.__name__)
            self.logger = logging.getLogger(self.logger_name)
            self.dblogging = None
            self.launch_date = pd.Timestamp.utcnow().tz_convert(tz=None)

            # Set root logger to required log level explicitly. Otherwise the log level of the calling environment is active.
            if log_level is not None:
                logging.getLogger().setLevel(log_level)

            self.production_mode = production_mode
            self.log_keep_days = log_keep_days
            self.is_icp = ICP_ENVIRONMENT_VARIABLE is not None and ICP_ENVIRONMENT_VARIABLE.lower() == "true"
            self.tenant_id = tenant_id
            self.entity_type_id = entity_type_id

            self.running_with_backtrack = False
            self.ignore_cache = False

            self.catalog = Catalog()

            self.granularities = dict()
            self.granularities_local = dict()
            self.pipeline = list()
            self.pipeline_local = list()

            # dict of target data item name to list of grain dimensions
            # mainly used when persiting to KPI tables, need to know the grain dimensions
            self.target_grains = defaultdict(list)
            self.target_grains_local = defaultdict(list)
            self.checkpoints_to_upsert = defaultdict(dict)

            # create an iotfunctions database connection and entity_type
            self.db = Database(tenant_id=tenant_id, entity_type_id=self.entity_type_id)
            self.db_type = self.db.db_type
            self.is_postgre_sql = False if self.db_type == 'db2' else True
            self.db_connection = self.db.native_connection
            self.db_connection_dbi = self.db.native_connection_dbi
            self.model_store = self.db.model_store

            self._init_service(engine_input)

            # Compose path for logfile in COS.  The log file names format: <tenant-id>/<entity-type>/YYYYmmdd/HHMMSS
            self.log_file_path = '%s/%s/%s/%s.gz' % (
                tenant_id, self.entity_type, self.launch_date.to_pydatetime().strftime('%Y%m%d'),
                self.launch_date.to_pydatetime().strftime('%H%M%S'))

            # Enable logging into database table as early as possible on package-level
            if dblogging_enabled is True:
                self.dblogging = dblogging.DBLogging(self.schema, self.entity_type_id, self.db_connection,
                                                     self.log_file_path, self.launch_date, self.local_log_file_name,
                                                     self.db_type, production_mode)

            self.catalog.load_custom_functions(catalog_functions=self._entity_catalog_functions)

            # Setup data cache
            self.cache = dbtables.DBDataCache(self.tenant_id, self.entity_type_id, self.schema, self.db_connection,
                                              self.db_type)

            kwargs = {'logical_name': self.entity_type, '_timestamp': self.eventTimestampColumn,
                      '_dimension_table_name': self.dimensionTable, '_entity_type_id': self.entity_type_id,
                      '_db_connection_dbi': self.db_connection_dbi, '_db_schema': self.schema,
                      '_data_items': self.data_items, 'tenant_id': tenant_id, '_db_connection': self.db_connection}

            #  Constants :: These are arbitrary parameter values provided by the server and copied onto the entity type
            logger.debug('Constants: {constant_name} = {constant_value}')
            for constant in self._entity_constants:
                key = constant['name']
                if isinstance(constant['value'], dict):
                    value = constant['value'].get('value', constant['value'])
                else:
                    value = constant['value']
                kwargs[key] = value
                logger.debug("%20s = %s" % (key, value))

            self.entity_type_obj = EntityType(self.eventTable, self.db, **kwargs)

        except BaseException as exception:
            self._log_exception(AnalyticsService.INIT_FAILURE_MESSAGE, exception)
            self.release_resource()
            raise

    def execute_kpi_pipelines(self, df=None, local_only=False):

        try:
            start_ts = None

            all_backpoints = []
            all_granularities = self.granularities.copy()
            all_granularities.update(self.granularities_local)
            result_dfs = AnalyticsServiceResult(all_granularities)

            pipeline = self.get_pipeline(local_only=local_only)

            if len(pipeline) == 0:
                return result_dfs

            # parse all KPI configuration to get their dependency tree as a dependency-ordered list
            queue = self.get_kpi_dependency_tree_processing_queue(pipeline)

            # Get last execution time from CHECK_POINT table
            # Be aware: last_execution_time can be None if there is no entry in CHECK_POINT table!
            last_execution_time = self.get_last_execution_time()

            # Calculate Backtrack and handle schedules
            scheduled_and_up = set()
            scheduled_but_not_up = set()
            not_scheduled = set()
            skipped = set()
            not_skipped = set()

            # first, identify those with schedules and whether the schedule is up or not
            for kpi_tree_node in queue:
                if kpi_tree_node.kpi.get('schedule') is not None:
                    if util.is_schedule_up(batch_start=last_execution_time, batch_end=self.launch_date,
                                           interval_start=kpi_tree_node.kpi['schedule'].get('starting_at'),
                                           interval=kpi_tree_node.kpi['schedule'].get('every')):
                        scheduled_and_up.add(kpi_tree_node)
                    else:
                        scheduled_but_not_up.add(kpi_tree_node)
                else:
                    not_scheduled.add(kpi_tree_node)

            self.logger.debug('KPIs without schedule: %s' % str([t.name for t in not_scheduled]))
            self.logger.debug('KPIs with due schedule: %s' % str([t.name for t in scheduled_and_up]))
            self.logger.debug('KPIs with undue schedule: %s' % str([t.name for t in scheduled_but_not_up]))

            # for not-up-scheduled, find if any of its descendants cannot be skipped (hence it cannot be skipped)
            if len(scheduled_but_not_up) > 0:
                self.logger.info('The following KPIs are eligible to be skipped according to their schedule:')
                for kpi_tree_node in scheduled_but_not_up:
                    self.logger.info('%s kpi_function: %s every: %s starting_at: %s' % (
                        kpi_tree_node.name, kpi_tree_node.kpi['functionName'],
                        kpi_tree_node.kpi['schedule'].get('every'), kpi_tree_node.kpi['schedule'].get('starting_at')))

                for kpi_tree_node in scheduled_but_not_up:
                    descendants = kpi_tree_node.get_all_descendants()
                    self.logger.debug('descendants: %s -> %s descendants that are not skipped: %s' % (
                        kpi_tree_node.name, str([t.name for t in descendants]),
                        str([t.name for t in descendants if t not in scheduled_but_not_up])))
                    if all([node in scheduled_but_not_up for node in descendants]):
                        skipped.add(kpi_tree_node)
                    else:
                        not_skipped.add(kpi_tree_node)

                self.logger.debug('KPIs with undue schedule that are skipped: %s' % str([t.name for t in skipped]))
                self.logger.debug('KPIs with undue schedule that are eligible to be skipped according to their '
                                  'schedule but cannot be skipped because of dependency to non-skipped KPIs: %s' % str(
                    [t.name for t in not_skipped]))

            # we can remove the skipped ones from the tree
            for kpi_tree_node in skipped:
                queue.remove(kpi_tree_node)

            # Terminate pipeline if there are no KPIs left to be processed (because of scheduling)
            if len(queue) == 0:
                # No KPIs to be processed. We can finish the pipeline here.
                if self.dblogging is not None:
                    # Set number of stages in logging table to 0
                    self.dblogging.set_total_stages(0)

                    # Final update of log entry in database about the successful run
                    self.dblogging.final_update_success()

                logger.info(AnalyticsService.SUCCESS_MESSAGE_NOTHING_TO_DO)
                return

            # finally, determine the backtrack range based on all KPIs that are not skipped, if there's any.
            # take the maximum range
            for kpi_tree_node in queue:
                schedule_starting_at = {}
                if kpi_tree_node.kpi.get('schedule') is not None:
                    starting_at = kpi_tree_node.kpi.get('schedule').get('starting_at')
                    if starting_at is None:
                        raise Exception(('The configuration of schedule for kpi %s is incomplete because the '
                                         'keyword starting_at is missing.') % kpi_tree_node.name)
                    if re.match('\d{1,2}:\d{2}(:\d{2})?', starting_at) is not None:
                        hour, minute, second = starting_at.split(':')
                        schedule_starting_at = {'hour': int(hour), 'minute': int(minute), 'second': int(second),
                                                'microsecond': 0, 'nanosecond': 0}
                    else:
                        date_string, time_string = starting_at.split(' ')
                        # year, month, day = date_string.split('-')
                        hour, minute, second = time_string.split(':')
                        schedule_starting_at = {'hour': int(hour), 'minute': int(minute), 'second': int(second),
                                                'microsecond': 0, 'nanosecond': 0}

                if kpi_tree_node.kpi.get('backtrack') is not None:
                    try:
                        # Add missing time-related labels to backtrack (DateOffset definition): For example,
                        # if backtrack contains 'minute' add all shorter units like 'second=0',
                        # 'microsecond=0' and 'nanosecond=0' if they are not explicitly given in backtrack.
                        # Especially 'second' and 'microsecond' are not provided by the configuration but are
                        # mandatory to exactly hit the boundary of, for example, a shift begin.
                        backtrack = kpi_tree_node.kpi.get('backtrack')
                        backtrack_keys = backtrack.keys()
                        label_found = False
                        for label in ['hour', 'minute', 'second', 'microsecond', 'nanosecond']:
                            if label in backtrack_keys:
                                label_found = True
                            elif label_found:
                                backtrack[label] = 0
                        # schedule_starting_at (if defined) overwrites schedule in backtrack
                        backtrack = {**backtrack, **schedule_starting_at}
                        offset = pd.tseries.offsets.DateOffset(**backtrack)
                        all_backpoints.append(self.launch_date - offset)
                    except BaseException:
                        self.logger.warning('invalid_backtrack_offset=%s, kpi=%s' % (
                            kpi_tree_node.kpi.get('backtrack'), kpi_tree_node.kpi), exc_info=True)

            if len(all_backpoints) > 0:
                self.running_with_backtrack = True
                start_ts = min(all_backpoints)
                self.logger.debug('earliest_backpoints=%s, all_backpoints=%s' % (str(start_ts), str(all_backpoints)))

            # group all KPIs based on their granularity
            all_aggregators = self.catalog.get_aggregators()
            grain_sequence_dependency_queue = defaultdict(
                set)  # keyed by grain with values of those grains depending on the keyed grain
            aggregation_configs = defaultdict(dict)
            non_aggregation_configs = list()

            non_agg_queue_debug_string = 'kpi_stage_processing_nonagg_queue = '
            for kpi_tree_node in queue:
                method = kpi_tree_node.kpi[KPI_FUNCTION_FUNCTIONNAME_KEY]
                granularity = kpi_tree_node.kpi.get(KPI_FUNCTION_GRANULARITY_KEY, None)

                if method in all_aggregators or granularity is not None:
                    # for aggregators or for transformers depend on aggregators
                    grain_dependency = None
                    for dep in kpi_tree_node.dependency:
                        if dep.kpi is not None:
                            depGrain = dep.kpi.get(KPI_FUNCTION_GRANULARITY_KEY, None)
                            # if depGrain is not None and depGrain != granularity:
                            if depGrain is not None:
                                grain_dependency = depGrain
                                # it is assumed all dependencies must have the same granularity
                                break

                    # add current granularity to the set that depends on grain_dependency
                    grain_sequence_dependency_queue[grain_dependency].add(granularity)

                    if kpi_tree_node not in set(aggregation_configs[granularity].setdefault(grain_dependency, [])):
                        # protection against same item having more than one dependencies, since we start 
                        # bottom up, this same item would be added more than once (one per dependency)
                        aggregation_configs[granularity].setdefault(grain_dependency, []).append(kpi_tree_node)
                else:
                    # transformer on its own
                    if kpi_tree_node.dependency is None or len(kpi_tree_node.dependency) == 0:
                        non_aggregation_configs.insert(0, kpi_tree_node.kpi)
                    else:
                        non_aggregation_configs.append(kpi_tree_node.kpi)
                    non_agg_queue_debug_string += '\n    %s, func=%s' % (kpi_tree_node, method)
            self.logger.debug(non_agg_queue_debug_string)

            if self.logger.isEnabledFor(logging.DEBUG):
                agg_queue_debug_string = 'kpi_stage_processing_agg_queue='
                for k, v in aggregation_configs.items():
                    agg_queue_debug_string += '\n    %s={' % str(k)
                    for depg, lst in v.items():
                        agg_queue_debug_string += '\n        %s:[' % str(depg)
                        for vv in lst:
                            agg_queue_debug_string += '\n            %s,' % str(vv)
                    agg_queue_debug_string += '\n    ]}'
                self.logger.debug(agg_queue_debug_string)

            grain_sequence = list()

            self.logger.debug('grain_sequence_dependency_queue=%s' % dict(grain_sequence_dependency_queue))
            for grain in grain_sequence_dependency_queue[None]:
                if grain not in grain_sequence:
                    grain_sequence.append(grain)
                for g in [g for g in grain_sequence_dependency_queue.get(grain, []) if g != grain]:
                    if g in grain_sequence:
                        grain_sequence.remove(g)
                    grain_sequence.append(g)

            grain_sequence = list()

            # figure out the grain level dependency
            grain_nodes = dict()
            for grain, depGrains in grain_sequence_dependency_queue.items():
                if grain not in grain_nodes:
                    grain_nodes[grain] = KpiTreeNode(grain, None, [])
                for depGrain in depGrains:
                    if depGrain != grain:
                        if depGrain not in grain_nodes:
                            grain_nodes[depGrain] = KpiTreeNode(depGrain, None, [])
                        grain_nodes[depGrain].dependency.append(grain_nodes[grain])
            leveled_items = defaultdict(list)
            for grain, tn in grain_nodes.items():
                if tn.tree_level() == 1 and tn.name is not None:
                    grain_sequence.append(tn.name)
                elif tn.tree_level() > 1:
                    leveled_items[tn.tree_level()].append(tn)
            for level in sorted(leveled_items.keys()):
                for tn in leveled_items[level]:
                    grain_sequence.append(tn.name)

            self.logger.debug('grain_sequence=%s' % str(list(grain_sequence)))

            if self.dblogging is not None:
                total_stage_count = self._calculate_total_stages(non_aggregation_configs, aggregation_configs)
                self.dblogging.set_total_stages(total_stage_count)

            pipeline_engine = CalcPipeline(
                self.generate_pipeline_stages(non_aggregation_configs, start_ts=self.launch_date),
                entity_type=self.entity_type_obj, dblogging=self.dblogging)

            # process overrides to start and end ts
            start_ts_override = self.entity_type_obj.get_start_ts_override()
            if start_ts_override is not None:
                start_ts = start_ts_override
            end_ts_override = self.entity_type_obj.get_end_ts_override()
            if end_ts_override is not None:
                end_ts = end_ts_override
            else:
                end_ts = None

            # process preload stages first if there are any
            (stages, preload_item_names) = pipeline_engine._execute_preload_stages(start_ts=start_ts, end_ts=end_ts,
                                                                                   entities=self.entity_type_obj.get_entity_filter())
            # replace the pipeline stages (removing those already done as a preload operation)
            pipeline_engine.set_stages(stages)
            self.logger.debug('removed preload stages from pipeline')

            if self.entity_type_obj._auto_read_from_ts_table and df is None:

                df = self.get_data(start_ts=start_ts, end_ts=end_ts, pipeline_obj=pipeline_engine,
                                   entities=self.entity_type_obj.get_entity_filter())

                # there are 2 methods for retrieving entity time series data prior to calculation  # choice of methods depend on how entity type was configured  # if self.entity_type_obj._checkpoint_by_entity:  #    # legacy api method  #    df = self.get_data(start_ts=start_ts, end_ts=end_ts, pipeline_obj=pipeline_engine,  #                       entities=self.entity_type_obj.get_entity_filter())  # else:  #    # iotfunctions get_data() method supports aggregation and uses common checkpoint  #    if start_ts is None:  #        start_ts = self.entity_type_obj.get_last_checkpoint()  #    # work out which data items are needed  #    all_granularities = self.granularities.copy()  #    all_granularities.update(self.granularities_local)  #    pipeline = self.get_pipeline()  #    data_items = (self.get_all_kpi_sources(pipeline) | get_all_granularity_dimensions(pipeline,  #                                                                                      all_granularities)) & self.data_items.get_raw_metrics()  #    data_items = data_items | pipeline_engine.get_input_items()  #    df = self.entity_type_obj.get_data(start_ts=start_ts, end_ts=end_ts,  #                                       entities=self.entity_type_obj.get_entity_filter(),  #                                       columns=data_items)
            elif df is not None:
                df = df.copy()
            else:
                df = pd.DataFrame()

            result_dfs[None] = pipeline_engine.execute(df, dropna=False, start_ts=start_ts, end_ts=end_ts,
                                                       entities=self.entity_type_obj.get_entity_filter(),
                                                       preloaded_item_names=preload_item_names)

            already_handled = set()
            for grain in grain_sequence:
                agg_transformers = list()

                results = list()
                for dep_grain, queue in aggregation_configs[grain].items():

                    self.logger.debug('current_grain=%s, dependent_grain=%s' % (grain, dep_grain))

                    stages_config = list()
                    for kpi_tree_node in queue:
                        if kpi_tree_node in already_handled:
                            continue
                        already_handled.add(kpi_tree_node)

                        method = kpi_tree_node.kpi[KPI_FUNCTION_FUNCTIONNAME_KEY]

                        if method not in all_aggregators:
                            if {depnode.name for depnode in kpi_tree_node.dependency}.issubset(set(grain[1])):
                                agg_transformers.insert(0, kpi_tree_node.kpi)
                            else:
                                agg_transformers.append(kpi_tree_node.kpi)
                        else:
                            stages_config.append(kpi_tree_node.kpi)

                    if grain == dep_grain:
                        if len(stages_config) > 0:
                            self.logger.warning(
                                'An aggregation on top of the same aggregation is not supported. The following KPIs are ignored: %s' % str(
                                    stages_config))
                        continue

                    if self.dblogging is not None:
                        self.dblogging.update_stage_info('InitializeGrain')

                    if result_dfs[dep_grain] is not None:
                        tmp_df = result_dfs[dep_grain].copy()

                        tmp_df = AggregationReloadUpdate(self, timestamp=self.eventTimestampName if grain[
                                                                                                        0] is not None else None,
                                                         granularity=grain, cache=self.cache, concat_only=False,
                                                         production_mode=self.production_mode).execute(tmp_df,
                                                                                                       dep_grain, grain)

                        pipeline_engine = CalcPipeline(
                            self.generate_pipeline_stages(stages_config, start_ts=self.launch_date),
                            entity_type=self.entity_type_obj, dblogging=self.dblogging)
                        results.append(pipeline_engine.execute(tmp_df, dropna=False, start_ts=start_ts))
                    else:
                        results.append(None)

                result_is_complete = True
                for ll in results:
                    if ll is None:
                        result_is_complete = False

                if result_is_complete:
                    # Merge all results from different source grains to this destination grain
                    result_dfs[grain] = pd.concat(results, axis=1, sort=False)
                    self.logger.info('All aggregations for grain %s have been calculated successfully.' % str(grain))

                    # Calculate transformers on top of aggregation result
                    if len(agg_transformers) > 0:
                        if self.dblogging is not None:
                            self.dblogging.update_stage_info('InitializeTransformerOnGrain')

                        self.logger.debug(
                            'Calculating agg_transformers=%s for grain %s' % (str(agg_transformers), grain))

                        pipeline_engine = CalcPipeline(
                            self.generate_pipeline_stages(agg_transformers, start_ts=self.launch_date),
                            entity_type=self.entity_type_obj, dblogging=self.dblogging)
                        result_dfs[grain] = pipeline_engine.execute(result_dfs[grain], dropna=False)

                else:
                    # The result set for destination grain is incomplete. Discard any result for this destination grain
                    # although they have already been persisted to database but the incomplete result is not a good
                    # base for further calculations (there is a risk of missing columns in data frame)
                    result_dfs[grain] = None
                    self.logger.info(
                        'Some aggregations for grain %s have been skipped because there were no new data. All calculations based on this grain are skipped as well.' % str(
                            grain))

            if self.dblogging is not None:
                self.dblogging.update_stage_info('FinalizePipeline')

            self.upsert_checkpoints(now=self.launch_date)

            self._update_granularitystatus()

            self.logger.info('pipeline total execution time (seconds) = %s' % (
                    pd.Timestamp.utcnow().tz_convert(tz=None) - self.launch_date).total_seconds())

            # close any connections opened by the entity type
            self.entity_type_obj.db.commit()

            self._log_pipeline_execution_result(result_dfs)

            logger.info(AnalyticsService.SUCCESS_MESSAGE)

            if self.dblogging is not None:
                # Final update of log entry in database about the successful run
                self.dblogging.final_update_success()

        except BaseException as exception:
            self._log_exception(AnalyticsService.FAILURE_MESSAGE, exception)
            raise

        return result_dfs

    def publish_execution_log_file(self):
        if self.production_mode and not self.is_icp and self.local_log_file_name is not None:
            logger.info('Logfile will be pushed to ObjectStore under \'%s\'' % self.log_file_path)

            try:
                if COS_BUCKET_LOGGING is not None:
                    log_files_to_drop = []
                    delete_log_from_date = dt.datetime.strptime(
                        (self.launch_date.to_pydatetime() - dt.timedelta(days=self.log_keep_days + 1)).strftime(
                            '%Y%m%d'), '%Y%m%d')
                    logger.debug('Deleting the COS logs before { %s }' % delete_log_from_date)

                    cos_log_file_paths = cos.cos_find('%s/%s' % (self.tenant_id, self.entity_type),
                                                      bucket=COS_BUCKET_LOGGING)
                    for cos_log_file_path in cos_log_file_paths:
                        cos_log_file_path_split = cos_log_file_path.split('/')
                        cos_log_file_path_date = dt.datetime.strptime(cos_log_file_path_split[2], '%Y%m%d')
                        if cos_log_file_path_date < delete_log_from_date:
                            log_files_to_drop.append(cos_log_file_path)

                    if len(log_files_to_drop) > 0:
                        logger.debug('Deleting the following cos log files %s' % log_files_to_drop)
                        cos.cos_delete_multiple(log_files_to_drop, bucket=COS_BUCKET_LOGGING)
                    else:
                        logger.debug('There is no old cos log file to delete.')

                    with open(self.local_log_file_name, 'r') as file:
                        cos.cos_put(self.log_file_path, gzip.compress(file.read().encode()), bucket=COS_BUCKET_LOGGING)
                else:
                    logger.warning('COS_BUCKET_LOGGING is not available. Logfile could not be pushed to ObjectStore.')
            except Exception as ex:
                logger.warning('Logfile could not be pushed to ObjectStore.', exc_info=True)

    def get_data(self, data_items=None, start_ts=None, end_ts=None, entities=None, pipeline_obj=None):
        """Get data from data lake.

        Optionally, filtering by the given data items, start/end timestamp, or entities.

        Normally when running in production mode, none of the 4 kwargs are given. They 
        are given when either running in non-production mode, or in special situation 
        like reprocessing history. Normal checkpointing should be suspended (or even 
        reset) in those situations.

        When not in production, and none of the 4 kwargs is given, it loads full history 
        of data items based on current KPI configuraiton.
        """
        if entities is None:
            entities = self.entity_type_obj.get_entity_filter()

        try:
            t1 = pd.Timestamp.utcnow()

            # if any of these kwarg is given, then we cannot use/update checkpoint anymore
            force_mode = any([param is not None for param in [data_items, start_ts, end_ts, entities]])

            # Use source definitions from KPI declarations if data_items isn't set
            loader_stage = None
            if data_items is None:
                all_granularities = self.granularities.copy()
                all_granularities.update(self.granularities_local)
                pipeline = self.get_pipeline()
                data_items = (self.get_all_kpi_sources(pipeline) | get_all_granularity_dimensions(pipeline,
                                                                                                  all_granularities)) & self.data_items.get_raw_metrics()
                if pipeline_obj is not None:
                    data_items = data_items | pipeline_obj.get_input_items()
                loader_stage = self.generate_loader_stage(pipeline=pipeline)

            events_and_metrics = self.data_items.get_names([DATA_ITEM_TYPE_METRIC, DATA_ITEM_TYPE_EVENT]) & set(
                data_items)
            dimensions = self.data_items.get_names(DATA_ITEM_TYPE_DIMENSION) & set(data_items)

            self.logger.debug('data_items=%s, start_ts=%s, end_ts=%s, entities=%s' % (
                str(data_items), str(start_ts), str(end_ts), str(entities)))
            self.logger.info(
                'raw_data_items=%s, dimension_data_items=%s' % (sorted(events_and_metrics), sorted(dimensions)))

            df = pd.DataFrame(columns=set([self.entityIdName, self.eventTimestampName] + list(events_and_metrics)))
            df = df.astype({self.entityIdName: str, self.eventTimestampName: 'datetime64[ns]'})

            # load metric data
            if len(events_and_metrics) > 0:

                if end_ts is None:
                    end_ts = self.launch_date.strftime(SQL_TIMESTAMP_FORMAT)

                checkpoint_helper = None
                if force_mode:
                    self.clean_checkpoints(data_items=events_and_metrics, entities=entities)
                    self.ignore_cache = True
                    if self.production_mode is True:
                        self.cache.delete_all_caches()
                else:
                    # normal production mode, get the time range from checkpoints
                    checkpoint_helper = self.get_checkpoints(data_items=events_and_metrics,
                                                             launch_date=self.launch_date)
                    start_ts = checkpoint_helper.get_common_start_for_updated_entities()
                    if start_ts is None:
                        start_ts = checkpoint_helper.get_common_start_for_updated_stale_entities()
                    if checkpoint_helper.get_checkpoints().empty:
                        self.ignore_cache = True
                        if self.production_mode is True:
                            self.cache.delete_all_caches()

                # for non-production mode, this is the only place for loading data
                if checkpoint_helper is not None and not checkpoint_helper.has_no_updated_entities() or force_mode:  # for special runs, this is the only loading place
                    existing_entities = None
                    if entities is not None:
                        existing_entities = entities
                    elif checkpoint_helper is not None:
                        existing_entities = checkpoint_helper.get_updated_entities()

                    df_raw = self.get_metric_data(events_and_metrics, start_ts, end_ts, existing_entities)
                    self.logger.debug(
                        'updated_entities=%s, start_ts=%s, end_ts=%s' % (existing_entities, start_ts, end_ts))
                    log_data_frame('updated_entities_df', df_raw.head())

                    df = df_raw

                if checkpoint_helper is not None and not checkpoint_helper.has_no_updated_stale_entities():
                    updated_stale_entities = checkpoint_helper.get_updated_stale_entities()
                    df_raw = self.get_metric_data(events_and_metrics,
                                                  checkpoint_helper.get_common_start_for_updated_stale_entities(),
                                                  end_ts, updated_stale_entities)
                    self.logger.debug('updated_stale_entities=%s, start_ts=%s, end_ts=%s' % (
                        updated_stale_entities, checkpoint_helper.get_common_start_for_updated_stale_entities(),
                        end_ts))
                    log_data_frame('updated_stale_entities_df', df_raw.head())

                    if df_raw.empty:
                        self.logger.debug('empty updated_stale_entities_data')
                    else:
                        df = pd.concat([df, df_raw], sort=False)
                        log_data_frame('updated_stale_entities_merged_df', df.head())

                # kohlmann Temporary removal to avoid 'start date == None' for GBS
                if not self.tenant_id.startswith('Sandvik'):
                    if checkpoint_helper is not None and not checkpoint_helper.has_no_new_entities():
                        new_entities = checkpoint_helper.get_new_entities()
                        df_raw = self.get_metric_data(events_and_metrics, None, end_ts, new_entities)
                        self.logger.debug('new_entities=%s, start_ts=%s, end_ts=%s' % (new_entities, None, end_ts))
                        log_data_frame('new_entities_df', df_raw.head())

                        if df_raw.empty:
                            self.logger.debug('empty new_entities_data')
                        else:
                            df = pd.concat([df, df_raw], sort=False)
                            log_data_frame('new_entities_merged_df', df.head())

                # since we load multiple devices with a single SQL query and not all devices are in sync in sending
                # data, some devices could have already processed data loaded again. here we further filter out
                # those already processed data (if they are older than the checkpointed per-device last processing time)
                if checkpoint_helper is not None and not checkpoint_helper.get_checkpoints().empty:
                    tmp_col_name = None
                    if KPI_ENTITY_ID_COLUMN in df.columns:
                        # Avoid column name clash in subsequent merge for KPI_ENTITY_ID_COLUMN
                        tmp_col_name = KPI_ENTITY_ID_COLUMN + UNIQUE_EXTENSION_LABEL
                        df = df.rename(columns={KPI_ENTITY_ID_COLUMN: tmp_col_name})
                    df = df.merge(checkpoint_helper.get_checkpoints(), how='left', left_on=self.entityIdName,
                                  right_on=KPI_ENTITY_ID_COLUMN, sort=False)
                    df['last_timestamp'] = df['last_timestamp'].fillna(
                        pd.Timestamp.min)  # for all new devices, timestamp will be null. We need to fill up NAT values
                    df = df[df[self.eventTimestampName] > df['last_timestamp']]
                    df.drop(columns=['last_timestamp', KPI_ENTITY_ID_COLUMN], inplace=True)
                    # Revert temporary name change
                    df = df.rename(columns={tmp_col_name: KPI_ENTITY_ID_COLUMN}, copy=False)

            # if any loader, call them to load external data
            if loader_stage is not None:
                df = df.set_index([self.entityIdName, self.eventTimestampName])
                df = loader_stage.execute(df, start_ts=start_ts, end_ts=end_ts, entities=entities)
                df = df.reset_index()

            # add dimension data
            if self.dblogging is not None:
                self.dblogging.update_stage_info('LoadingDimensions')

            if len(dimensions) > 0:
                df_dimension = self.get_dimension_data(dimensions, entities)
                if df_dimension.empty:
                    self.logger.debug('empty dimension_data')
                else:
                    df = df.merge(df_dimension, how='left', left_on=self.entityIdName, right_on=self.entityIdName,
                                  sort=False)
                    log_data_frame('dimension_merged_df', df.head())

                    # for raw data, we always set index to be (id, timestamp)
            df = df.set_index([self.entityIdName, self.eventTimestampName])

            t2 = pd.Timestamp.utcnow()
            self.logger.info('get_data_time_seconds=%s' % (t2 - t1).total_seconds())
        except Exception as ex:
            self.logger.error('Retrieval of data failed.', exc_info=True)
            raise

        # uncomment only after testing better
        # Optimizing the data frame size using downcasting
        # memo = MemoryOptimizer()
        # df = memo.downcastNumeric(df)
        # memo.downcastNumeric(df)

        return df

    def get_params(self):
        """
        Get metadata parameters
        """
        params = {'_entity_type_logical_name': self.entity_type, 'entity_type_name': self.eventTable,
                  '_timestamp': self.eventTimestampColumn, 'db': None, '_dimension_table_name': self.dimensionTable,
                  '_db_connection_dbi': self.db_connection_dbi, '_db_schema': self.schema,
                  '_data_items': self.data_items}
        return params

    def get_pipeline(self, local_only=False):
        if local_only:
            all_local_targets = get_all_kpi_targets(self.pipeline_local)

            self.logger.info('all_local_targets=%s' % str(all_local_targets))

            all_local_dependencies = set()
            kpi_tree = self.parse_kpi_dependency_tree(pipeline=(self.pipeline + self.pipeline_local))[0]
            for name, treenode in kpi_tree.items():
                if name in all_local_targets:
                    all_local_dependencies.add(treenode)
                    all_local_dependencies.update(treenode.get_all_dependencies())

            self.logger.info('all_local_dependencies=%s' % str(all_local_dependencies))

            filtered_tree = dict()
            for name, treenode in kpi_tree.items():
                if treenode in all_local_dependencies:
                    filtered_tree[name] = treenode

            self.logger.info('filtered_tree=%s' % str(filtered_tree))

            filtered_names = set(filtered_tree.keys())

            pipeline = self.pipeline_local.copy()
            for kpi in self.pipeline:
                targets = get_kpi_targets(kpi)
                if any([t in filtered_names for t in targets]):
                    pipeline.append(kpi)

            self.logger.info('pipeline=%s' % str(pipeline))

            return pipeline
        else:
            return self.pipeline + self.pipeline_local

    def reset_pipeline(self):
        """Reset the pipeline to the initial server based state."""
        self.granularities_local = dict()
        self.pipeline_local = list()
        self.target_grains_local = defaultdict(list)

    def add_granularity_set(self, name, frequency=None, data_items=None, entity_first=True):
        """Add a local granularity set, mainly for client side usage."""
        if data_items is not None and (
                not isinstance(data_items, list) or any([not isinstance(item, str) for item in data_items])):
            raise TypeError('data_items=%s must be either None or a list of string')

        self.granularities_local[name] = (frequency, tuple(data_items if data_items is not None else []), entity_first)

    def add_kpi(self, kpis):
        warnings.warn('add kpi function is deprecated.', DeprecationWarning)
        """Add one or multiple local kpi, mainly for client side usage."""
        if isinstance(kpis, dict):
            kpis = [kpis]
        elif not isinstance(kpis, list) or any([not isinstance(kpi, dict) for kpi in kpis]):
            raise TypeError('the given kpis must be either a dict or a list of dict')

        invalid_kpis = []
        for kpi in kpis:
            if not self._valid_new_kpi(kpi):
                invalid_kpis.append(kpi)
        if len(invalid_kpis) > 0:
            raise ValueError('invalid_kpis=%s' % str(invalid_kpis))

        for kpi in kpis:
            # default is enabled
            if KPI_FUNCTION_ENABLED_KEY not in kpi:
                kpi[KPI_FUNCTION_ENABLED_KEY] = True
            elif not kpi[KPI_FUNCTION_ENABLED_KEY]:
                # filter any disabled kpi
                continue

            # replace grain name with actual grain
            if kpi.get(KPI_FUNCTION_GRANULARITY_KEY) is not None:
                grain_name = kpi[KPI_FUNCTION_GRANULARITY_KEY]
                gran = self.granularities.get(grain_name)
                if gran is None:
                    gran = self.granularities_local.get(grain_name)
                kpi[KPI_FUNCTION_GRANULARITY_KEY] = gran

                for target in get_kpi_targets(kpi):
                    self.target_grains_local[target] = kpi[KPI_FUNCTION_GRANULARITY_KEY]

            self.pipeline_local.append(kpi)

    def push(self):
        warnings.warn('push function is deprecated.', DeprecationWarning)
        """Push local granularities and kpis to server.

        The dependency tree is used to determine the sequence of creation, otherwise server side 
        would reject it.
        """
        if len(self.granularities_local) == 0 and len(self.pipeline_local) == 0:
            return

        queue = self.get_kpi_dependency_tree_processing_queue(self.get_pipeline())
        grain_queue = self.granularities_local.copy()
        all_targets_to_push = get_all_kpi_targets(self.pipeline_local)

        for treenode in queue:
            kpi = treenode.kpi

            if kpi.get(KPI_FUNCTION_GRANULARITY_KEY) is not None:
                grain = kpi.get(KPI_FUNCTION_GRANULARITY_KEY)

                idx = -1
                try:
                    idx = list(grain_queue.values()).index(grain)
                except Exception:
                    pass

                if idx != -1:
                    grain_name = list(grain_queue.keys())[idx]
                    self.logger.info('pushing grain_name=%s, grain=%s' % (grain_name, str(grain)))
                    if not self._push_grain({"name": grain_name, "description": grain_name, "frequency": grain[0],
                                             "dataItems": list(grain[1]), "entityFirst": grain[2]}):
                        # fail fast because of dependency tree
                        raise RuntimeError(
                            'failed pushing grain_name=%s, grain=%s, stop pushing here' % (grain_name, str(grain)))

                    grain_queue.pop(grain_name)

            current_kpi_targets = set(get_kpi_targets(kpi))
            if current_kpi_targets.issubset(all_targets_to_push):
                self.logger.info('pushing treenode=%s' % treenode)
                if not self._push_kpi(kpi):
                    # fail fast because of dependency tree
                    raise RuntimeError('failed pushing treenode=%s' % treenode)

                all_targets_to_push -= current_kpi_targets

            if len(grain_queue) == 0 and len(all_targets_to_push) == 0:
                break

        self.reset_pipeline()
        self._init_service()

    def _valid_new_kpi(self, kpi):
        warnings.warn('add kpi function is deprecated.', DeprecationWarning)
        """Validate the given new KPI, mainly for client side usage."""
        if not isinstance(kpi, dict):
            return False

        # mandatory fields

        if KPI_FUNCTION_FUNCTIONNAME_KEY not in kpi:
            self.logger.warning('missing_kpi_field=%s of kpi=%s' % (KPI_FUNCTION_FUNCTIONNAME_KEY, str(kpi)))
            return False
        if KPI_FUNCTION_INPUT_KEY not in kpi:
            self.logger.warning('missing_kpi_field=%s of kpi=%s' % (KPI_FUNCTION_INPUT_KEY, str(kpi)))
            return False
        if KPI_FUNCTION_OUTPUT_KEY not in kpi:
            self.logger.warning('missing_kpi_field=%s of kpi=%s' % (KPI_FUNCTION_OUTPUT_KEY, str(kpi)))
            return False

        # is function name valid?
        if self.catalog.get_function(kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY)) is None:
            self.logger.warning(
                'invalid_functon_name=%s of kpi=%s' % (kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY), str(kpi)))
            return False

        # is grain name vlaid?
        if kpi.get(KPI_FUNCTION_GRANULARITY_KEY) is not None:
            grain_name = kpi[KPI_FUNCTION_GRANULARITY_KEY]
            if self.granularities.get(grain_name) is None and self.granularities_local.get(grain_name) is None:
                self.logger.warning('invalid_grain_name=%s of kpi=%s' % (grain_name, str(kpi)))
                return False

        # is any of the output matches existing data items?
        # 
        # this can only check against server side data items, note that we are still in the process of 
        # adding potentially many kpis and there's no dependency checking untile the end of this addition
        if not self.data_items.get_all_names().isdisjoint(set(get_kpi_targets(kpi))):
            self.logger.warning('invalid_duplicate_function_outputs=%s of kpi=%s' % (get_kpi_targets(kpi), str(kpi)))
            return False

        return True

    def _push_grain(self, grain):
        warnings.warn('push grain function is deprecated.', DeprecationWarning)
        resp = util.api_request(GRANULARITY_REQUEST_TEMPLATE.format(self.tenant_id, self.entity_type), method='post',
                                json=grain)
        if resp is None:
            self.logger.warning('error creating granularity_set=%s' % str(grain))
            return False
        return True

    def _update_granularitystatus(self):

        if self.production_mode is True:
            resp = util.api_request(GRANULARITY_SETSTATUS_TEMPLATE.format(self.tenant_id, self.entity_type),
                                    method='post', json=None)
            if resp is None:
                self.logger.warning('error updating granularity status')
                return False
            self.logger.info('Success in updating granularity Status...')

        return True

    def _push_kpi(self, kpi):
        warnings.warn('push kpi function is deprecated.', DeprecationWarning)
        resp = util.api_request(KPI_FUNCTION_REQUEST_TEMPLATE.format(self.tenant_id, self.entity_type), method='post',
                                json=kpi)
        if resp is None:
            self.logger.warning('error creating kpi_function=%s' % str(kpi))
            return False
        return True

    def register_function(self, module_and_target_name, url=None, name=None, local=True):
        warnings.warn('register catalog function is deprecated. Use register function from IOTFunction.',
                      DeprecationWarning)
        """Register the given function.

        Arguments
        module_and_target_name -- name of the target function, including package/module.

        Keyword arguments
        url -- the address from which the function's package can be retrieved, either 
               pointing to git repository or a egg file on the web, optional, if not 
               given, the function is assumed already installed locally and the 
               registration is local only
        name -- the unique name for identifying the function, optiona, default is the  
                function's class name
        local -- local registration or not.
        """
        if url is not None:
            if not self.catalog._install(url):
                return False
        else:
            # if no url given, this registration can only be local
            local = True

        func = self.catalog._get_class(module_and_target_name)

        if 'metadata' not in dir(func):
            raise TypeError('missing mandatory class function \'metadata\' in %s' % module_and_target_name)

        metadata = func.metadata()
        if name is not None:
            metadata[CATALOG_FUNCTION_NAME_KEY] = name

        if metadata[CATALOG_FUNCTION_CATEGORY_KEY] == self.catalog.CATEGORY_AGGREGATOR:
            registration_func = self.catalog.register_aggregator
        elif metadata[CATALOG_FUNCTION_CATEGORY_KEY] == self.catalog.CATEGORY_TRANSFORMER:
            registration_func = self.catalog.register_transformer

        return registration_func(name=metadata.get(CATALOG_FUNCTION_NAME_KEY),
                                 description=metadata.get(CATALOG_FUNCTION_DESCRIPTION_KEY),
                                 tags=metadata.get(CATALOG_FUNCTION_TAGS_KEY),
                                 module_and_target_name=metadata.get(CATALOG_FUNCTION_MODULETARGET_KEY),
                                 input_params=metadata.get(CATALOG_FUNCTION_INPUT_KEY),
                                 output_params=metadata.get(CATALOG_FUNCTION_OUTPUT_KEY),
                                 incremental_update=metadata.get(CATALOG_FUNCTION_INCUPDATE_KEY),
                                 url=None if local else url, tenant_id=None if local else self.tenant_id)

    def unregister_function(self, name, local=True):
        warnings.warn('un register catalog function is deprecated. Use register function from IOTFunction.',
                      DeprecationWarning)
        return self.catalog.unregister(name, tenant_id=None if local else self.tenant_id)

    def __del__(self):
        self.release_resource()

    def _log_exception(self, pipeline_execution_status, exception):
        error_message = str(exception)
        error_type = exception.__class__.__name__

        if error_type == 'StageException':
            error_stacktrace = exception.exception_details['stack_trace']
        else:
            error_stacktrace = traceback.format_exc()

        logger.error(error_message)
        logger.error(error_stacktrace)
        logger.error(pipeline_execution_status)

        if self.dblogging is not None:
            self.dblogging.final_update_error(error_type, error_message, error_stacktrace)

    def release_resource(self):
        try:
            db = getattr(self, 'db', None)
            if db is not None:
                db.release_resource()
        except Exception:
            self.logger.warning('Error while closing database connection.', exc_info=True)
        finally:
            self.db_connection = None

    def _get_engine_input(self, tenant_id, entity_type_id):
        engine_input_response = util.api_request(ENGINE_INPUT_REQUEST_TEMPLATE.format(tenant_id, entity_type_id))
        if engine_input_response is None:
            raise RuntimeError('Could not get engine input.')

        return engine_input_response.json()

    def _init_service(self, engine_input=None):
        if engine_input is None:
            engine_input = self._get_engine_input(self.tenant_id, self.entity_type_id)

        # Get details from table ENTITY TYPE
        self.entity_type = engine_input['entityTypeName']
        self.entity_type_id = engine_input['entityTypeId']
        self.default_db_schema = engine_input['defaultDBSchema']
        self.schema = engine_input['schemaName']
        self.eventTable = engine_input['metricsTableName']
        self.eventTimestampColumn = engine_input['metricTimestampColumn']
        self.entityIdColumn = ENTITY_ID_COLUMN
        self.dimensionTable = engine_input['dimensionsTable']

        self.entityIdName = DATAFRAME_INDEX_ENTITYID
        self.eventTimestampName = DEFAULT_DATAFRAME_INDEX_TIMESTAMP  # use default one if no such data item created

        # Get DATA ITEM details
        self.data_items = DataItemMetadata()
        if 'dataItems' in engine_input and engine_input['dataItems'] is not None:
            for dataItem in engine_input['dataItems']:
                dataItemName = dataItem[DATA_ITEM_NAME_KEY]

                self.data_items.add(dataItem)
                if (dataItem.get(DATA_ITEM_COLUMN_NAME_KEY, None) is not None and dataItem.get(
                        DATA_ITEM_COLUMN_NAME_KEY, '').upper() == self.eventTimestampColumn.upper()):
                    self.eventTimestampName = dataItemName

        self.logger.info(
            'entity_type_name= {{ %s }} , entity_type_id= {{ %s }}' % (self.entity_type, self.entity_type_id))
        self.logger.info(
            'entity_id_name= {{ %s }}, entity_id_column= {{ %s }}' % (self.entityIdName, self.entityIdColumn))
        self.logger.info('timestamp_name= {{ %s }}, timestamp_column= {{ %s }}' % (
            self.eventTimestampName, self.eventTimestampColumn))
        self.logger.info('dimension_data_items=%s, raw_data_items=%s, derived_data_items=%s' % (
            sorted(self.data_items.get_dimensions()), sorted(self.data_items.get_raw_metrics()),
            sorted(self.data_items.get_derived_metrics())))

        # Get time frquencies
        frequencies = dict()
        if 'frequencies' in engine_input:
            frequencies = engine_input['frequencies']
            frequencies = {v['name']: v['alias'] for v in frequencies}
        self.logger.info('frequencies=%s' % sorted(frequencies))

        # Get granularity sets
        self.granularities = dict()
        if 'granularities' in engine_input and engine_input['granularities'] is not None:
            granularities = engine_input['granularities']
            self.granularities = {v['name']: (
                frequencies.get(v['frequency'], None), tuple(v.get('dataItems', [])), v.get('entityFirst', True),
                v.get('granularitySetId')) for v in granularities}
        self.logger.info('granularities=%s' % sorted(self.granularities.items()))

        # Get KPI declarations
        self._set_pipeline(engine_input.get('kpiDeclarations', []))
        self._entity_constants = engine_input.get('constants', [])
        self._entity_catalog_functions = engine_input.get('catalogFunctions', [])

    def _set_pipeline(self, pipeline):
        if pipeline is None:
            pipeline = []

        # self.logger.debug('kpi_declarations=%s' % json.dumps(pipeline, sort_keys=True, indent=2))
        self.pipeline = [kpi for kpi in pipeline if kpi.get('enabled', False) == True]
        self.logger.info('kpi_declarations_filtered(enabled)=%s' % self.pipeline)

        self.target_grains = defaultdict(list)

        # replacing/filling grain name with actual grain data items
        for kpi in pipeline:
            if kpi.get(KPI_FUNCTION_GRANULARITY_KEY) is not None:
                gran = self.granularities[kpi[KPI_FUNCTION_GRANULARITY_KEY]]
                kpi[KPI_FUNCTION_GRANULARITY_KEY] = gran

                for target in get_kpi_targets(kpi):
                    self.target_grains[target] = kpi[KPI_FUNCTION_GRANULARITY_KEY]

        self.logger.info('kpi_target_grains=%s' % dict(self.target_grains))

    def _calculate_total_stages(self, non_aggregation_configs, aggregation_configs):
        # Count total number of stages for KPI_LOGGING table
        # pseudo stage FinalizePipeline, LoadingDimensions, LoadingRawMetrics, WritingUnmatchedEntities
        total_stage_count = 4
        if len(non_aggregation_configs) > 0:
            # Transformers on raw data + internal stages: PersistColumns, ProduceAlerts
            total_stage_count += len(non_aggregation_configs) + 2
            # Add one for stage RecordUsage when at least one loader is in pipeline
            loaders = self.catalog.get_loaders()
            if len(loaders) > 0:
                for kpi in non_aggregation_configs:
                    fname = kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY)
                    if fname in loaders:
                        total_stage_count += 1
                        break
        for dest_grain, agg_config in aggregation_configs.items():
            transformers_after_aggregation = 0
            for source_grain, item_list in agg_config.items():
                if source_grain == dest_grain:
                    # Transformers after an aggregation
                    transformers_after_aggregation += len(item_list)
                else:
                    # Stage Aggregation + internal stages: ProjectColumns, PersistColumns, ProduceAlerts,  pseudo stage InitializeGrain
                    total_stage_count += 5
            if transformers_after_aggregation != 0:
                # Transformers after an aggregation + internal stages: PersistColumns, ProduceAlerts,  + pseudo stage InitializeTransformerOnGrain
                total_stage_count += transformers_after_aggregation + 3

        return total_stage_count

    def _log_pipeline_execution_result(self, result_dfs):
        for g, df in result_dfs.items():
            if df is not None and not df.empty:
                if g is not None:
                    log_data_frame('Granularity = %s, result_aggregated_df' % str(g), df.head())
                else:
                    log_data_frame('result_non_aggregated_df', df.head())
            else:
                if g is not None:
                    self.logger.info('Grain %s has not been calculated because there were no input data' % str(g))
                else:
                    self.logger.info('Transformation has not been calculated because there were no input data')

    def get_last_execution_time(self):
        """Get the last execution time of the entity type.

        The checkpoint table uses a special row per type for recording the last executing of the type, with 
        empty string entity id and key.
        """
        sql = 'SELECT TIMESTAMP AS "last_timestamp" FROM %s.KPI_CHECKPOINT WHERE %s = %s AND %s = \'\''

        if self.db_type == 'db2':
            sql = sql % (dbhelper.quotingSchemaName(self.schema), dbhelper.quotingColumnName(KPI_ENTITY_TYPE_ID_COLUMN),
                         dbhelper.quotingSqlString(self.entity_type_id),
                         dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN))
        elif self.db_type == 'postgresql':
            sql = sql % (dbhelper.quotingSchemaName(self.schema, True),
                         dbhelper.quotingColumnName(KPI_ENTITY_TYPE_ID_COLUMN, True), self.entity_type_id,
                         dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN, True))

        df = self.db.read_sql_query(sql, log_message='get_last_execution_time')

        return None if df.empty else df.loc[0, 'last_timestamp']

    def get_checkpoints(self, data_items, launch_date):
        """Get checkpoint records.

        The way it does is first get the latest timestamp of each device from events table,
        then get the last processed timestamp of each device/metric from checkpoints table. Then take the maximum of 
        all metrics of an entity as the lastprocessing time for that entity. Then by comparing the per device last 
        processing time and the latest timestamp, we we know which device has new data. Finally, from within those 
        devices having new data, get the earliest last processed timestamp as the starting point to load data.

        For devices having new data, they are further divided into two groups. One with last processing time way back. 
        They could be "stale" for a while and then have new data coming in. In order to not cause all other "normal" 
        devices also load from a very long timestamp ago, we load them separately.
        """

        # first load from event table, per entity latest time
        df_chunks = []
        for di in data_items:
            di_metadata = self.data_items.get(di)
            if di_metadata is None or di_metadata.get(DATA_ITEM_COLUMN_NAME_KEY) is None:
                continue

            sql = 'SELECT %s AS "%s", MAX(%s) AS "latest_timestamp" FROM %s.%s WHERE %s IS NOT NULL GROUP BY %s' % (
                dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql), KPI_ENTITY_ID_COLUMN,
                dbhelper.quotingColumnName(
                    self.eventTimestampColumn.lower() if self.is_postgre_sql else self.eventTimestampColumn,
                    self.is_postgre_sql), dbhelper.quotingSchemaName(self.schema, self.is_postgre_sql),
                dbhelper.quotingTableName(self.eventTable, self.is_postgre_sql),
                dbhelper.quotingColumnName(di_metadata.get(DATA_ITEM_COLUMN_NAME_KEY), self.is_postgre_sql),
                dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql))

            df_chunks.append(self.db.read_sql_query(sql, parse_dates=['latest_timestamp'],
                                                    log_message='entity_last_timestamp').astype(
                {KPI_ENTITY_ID_COLUMN: str}, copy=False))

        df_events = pd.concat(df_chunks, ignore_index=True, sort=False)

        df_events['latest_timestamp'] = np.where(df_events['latest_timestamp'] > launch_date,
                                                 launch_date.to_datetime64(), df_events['latest_timestamp'])
        df_events = df_events.groupby([KPI_ENTITY_ID_COLUMN]).agg({'latest_timestamp': 'max'})
        df_events = df_events.reset_index()  # move entity id back to column

        log_data_frame('df_events', df_events.sort_values(by=[KPI_ENTITY_ID_COLUMN]).head())

        sql = 'SELECT %s AS "entity_id", KEY AS "metric", TIMESTAMP AS "last_timestamp" FROM %s.KPI_CHECKPOINT WHERE %s = %s AND %s <> \'\''
        if self.db_type == 'db2':
            # next, load from checkpoint table, per table/metric last processing time
            sql = sql % (dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN), dbhelper.quotingSchemaName(self.schema),
                         dbhelper.quotingColumnName(KPI_ENTITY_TYPE_ID_COLUMN),
                         dbhelper.quotingSqlString(self.entity_type_id),
                         dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN))
        elif self.db_type == 'postgresql':
            sql = sql % (
                dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN, True), dbhelper.quotingSchemaName(self.schema, True),
                dbhelper.quotingColumnName(KPI_ENTITY_TYPE_ID_COLUMN, True), self.entity_type_id,
                dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN, True))

        if data_items is not None and len(data_items) > 0:
            sql += ' AND KEY in (%s)' % ', '.join([dbhelper.quotingSqlString(key) for key in data_items])

        df_checkpoints = self.db.read_sql_query(sql, parse_dates=['last_timestamp'],
                                                log_message='entity_last_timestamp')

        # we assume the in order natrue per entity, so we simply take the max of last processing time of all metrics
        # of an entity as its last processing time
        df_checkpoints = df_checkpoints.groupby([KPI_ENTITY_ID_COLUMN]).agg({'last_timestamp': 'max'})
        df_checkpoints = df_checkpoints.reset_index()  # move entity id back to column

        log_data_frame('df_checkpoints', df_checkpoints.sort_values(by=[KPI_ENTITY_ID_COLUMN]).head())

        # by (inner) joining both dataframes, we can filter out and leave only entities having checkpoint records
        df_updated_entities = pd.merge(df_events, df_checkpoints, how='inner', on=KPI_ENTITY_ID_COLUMN).astype(
            {KPI_ENTITY_ID_COLUMN: str})
        if df_checkpoints.empty:
            df_updated_entities['gap'] = STALE_DEVICE_CRITERIA + 1
        else:
            df_updated_entities['gap'] = (df_updated_entities['latest_timestamp'] - df_updated_entities[
                'last_timestamp']) / np.timedelta64(1, 'm')
        df_updated_stale_entities = df_updated_entities.copy()

        # furthermore, filter out any such entity havingno new data since last processed
        if not df_updated_entities.empty:
            df_updated_entities = df_updated_entities[
                (0 < df_updated_entities['gap']) & (df_updated_entities['gap'] <= STALE_DEVICE_CRITERIA)]
            df_updated_stale_entities = df_updated_stale_entities[
                df_updated_stale_entities['gap'] > STALE_DEVICE_CRITERIA]

        # a problem with stale entities (not sending for a very long time) "resurrect" could cause a very
        # heavy reprocessing, since the starting time would be chosen to be its last processing time, we
        # pre-filter entities having too old "last_update" column value

        log_data_frame('df_updated_entities', df_updated_entities.sort_values(by=[KPI_ENTITY_ID_COLUMN]).head())
        log_data_frame('df_updated_stale_entities',
                       df_updated_stale_entities.sort_values(by=[KPI_ENTITY_ID_COLUMN]).head())

        # lastly, find out all entities without checkpoint records, that is, new entities
        df_new_entities = df_events[
            ~df_events[KPI_ENTITY_ID_COLUMN].isin(df_checkpoints[KPI_ENTITY_ID_COLUMN].unique())]

        log_data_frame('df_new_entities', df_new_entities.sort_values(by=[KPI_ENTITY_ID_COLUMN]).head())

        return CheckpointsHelper(df_checkpoints, df_updated_entities, df_updated_stale_entities, df_new_entities,
                                 self.db_type)

    def clean_checkpoints(self, data_items, entities):
        if self.production_mode:
            sql = 'DELETE FROM %s.kpi_checkpoint WHERE %s = %s' % (
                dbhelper.quotingSchemaName(self.schema, self.is_postgre_sql),
                dbhelper.quotingColumnName(KPI_ENTITY_TYPE_ID_COLUMN, self.is_postgre_sql),
                dbhelper.quotingSqlString(self.entity_type_id))
            if data_items is not None and len(data_items) > 0:
                sql += ' AND KEY IN (%s)' % ', '.join([dbhelper.quotingSqlString(key) for key in data_items])
            if entities is not None and len(entities) > 0:
                sql += ' AND %s in (%s)' % (dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN, self.is_postgre_sql),
                                            ', '.join([dbhelper.quotingSqlString(entity) for entity in entities]))
            self.logger.debug('clean_checkpoints_sql = %s' % sql)

            try:
                if self.db_type == 'db2':
                    ibm_db.exec_immediate(self.db_connection, sql)
                elif self.db_type == 'postgresql':
                    dbhelper.execute_postgre_sql_query(self.db_connection, sql)

                self.logger.info('Checkpoints have been deleted from KPI_CHECKPOINT table')
            except Exception:
                self.logger.warning('Error cleaning up checkpoints', exc_info=True)

    def add_checkpoint(self, metric_name, entity_id, ts):
        if metric_name not in self.checkpoints_to_upsert[entity_id]:
            self.checkpoints_to_upsert[entity_id][metric_name] = ts
        elif self.checkpoints_to_upsert[entity_id][metric_name] < ts:
            self.checkpoints_to_upsert[entity_id][metric_name] = ts

    def get_upsert_checkpoint_params(self, entity_type):
        valueList = []
        for entity, vals in self.checkpoints_to_upsert.items():
            for metric, ts in vals.items():
                t = ts, entity_type, entity, metric
                valueList.append(t)

        return valueList

    def create_checkpoint_entries(self, dataframe):
        if self.production_mode:
            # only raw metrics need to be processed (but not dimensions)
            raw_columns = set(dataframe.columns.values) & (
                    self.data_items.get_raw_metrics() - self.data_items.get_dimensions())
            # move self.entityIdName and self.eventTimestampName (and any granularity
            # dimensions but they are irrelevant here) to be columns for groupby
            df = dataframe[list(raw_columns)].reset_index()

            for metric_name in raw_columns:
                # get latest timestamp per device/metric
                df_latest = df.loc[
                    df.dropna(subset=[metric_name]).groupby([self.entityIdName])[self.eventTimestampName].idxmax()]

                for df_row in df_latest[[self.entityIdName, self.eventTimestampName]].itertuples(index=False,
                                                                                                 name=None):
                    # self.logger.debug("checkpoint entry: %s, %s, %s" % (metricName, row[self.entityIdName], row[self.eventTimestampName]))
                    self.add_checkpoint(metric_name, df_row[0], df_row[1])

    def upsert_checkpoints(self, now=None):
        if self.production_mode:
            value_list = self.get_upsert_checkpoint_params(self.entity_type_id)

            if now is not None:
                # for the per-type last execution time checkpointing
                value_list.append((now, self.entity_type_id, '', ''))

            self.logger.debug('checkpoints_to_upsert = %s' % value_list)

            if len(value_list) > 0:

                try:
                    if self.db_type == 'db2':
                        sql = ("MERGE INTO %s.KPI_CHECKPOINT AS TARGET "
                               "USING (VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)) AS SOURCE (TIMESTAMP, ENTITY_TYPE_ID, ENTITY_ID, KEY, LAST_UPDATE) "
                               "ON TARGET.ENTITY_TYPE_ID = SOURCE.ENTITY_TYPE_ID AND TARGET.ENTITY_ID = SOURCE.ENTITY_ID AND TARGET.KEY = SOURCE.KEY "
                               "WHEN MATCHED THEN "
                               "UPDATE SET TARGET.TIMESTAMP = SOURCE.TIMESTAMP, TARGET.LAST_UPDATE = SOURCE.LAST_UPDATE "
                               "WHEN NOT MATCHED THEN "
                               "INSERT (TIMESTAMP, ENTITY_TYPE_ID, ENTITY_ID, KEY, LAST_UPDATE) VALUES (SOURCE.TIMESTAMP, SOURCE.ENTITY_TYPE_ID, SOURCE.ENTITY_ID, SOURCE.KEY, CURRENT_TIMESTAMP)") % (
                                  dbhelper.quotingSchemaName(self.schema))
                        self.logger.debug('checkpoint_upsert_sql = %s' % sql)
                        stmt = ibm_db.prepare(self.db_connection, sql)
                        res = ibm_db.execute_many(stmt, tuple(value_list))  # Bulk insert

                        self.logger.debug(
                            'checkpoints_upserted = %s' % str(res) if res is not None else str(ibm_db.num_rows(stmt)))

                    elif self.db_type == 'postgresql':

                        sql = "insert into " + dbhelper.quotingSchemaName(self.schema,
                                                                          self.is_postgre_sql) + ".kpi_checkpoint (timestamp,entity_type_id,entity_id,key,last_update) values (%s,%s,%s,%s,current_timestamp) ON CONFLICT ON CONSTRAINT uc_key_kpi_checkpoint DO update set timestamp = EXCLUDED.timestamp, last_update = EXCLUDED.last_update"

                        self.logger.debug('checkpoint_upsert_sql = %s' % sql)

                        dbhelper.execute_batch(self.db_connection, sql, value_list)
                        self.logger.debug('checkpoints_upserted = %s' % len(value_list))

                except Exception:
                    self.logger.warning("error upsert checkpoints", exc_info=True)

    def get_metric_data(self, data_item_names, start_ts, end_ts, entities=None):
        """
        There is an upper bound on the SQL statement length allowed, hence we need to batch
        somehow and concatenate the resultant dataframes. The limit seems to be 2MB bytes which
        means roughly at least allow 20000~30000 entities per executiion.
        """
        requested_col_names = []
        tableColumns = list()
        df_chunks = []

        if entities is None or len(util.asList(entities)) == 0:
            entities = [None]

        if self.dblogging is not None:
            self.dblogging.update_stage_info('LoadingRawMetrics')

        start_time = pd.Timestamp.utcnow()

        # add entity id
        tableColumns.append("%s AS %s" % (dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql),
                                          dbhelper.quotingColumnName(self.entityIdName, self.is_postgre_sql)))
        requested_col_names.append(self.entityIdName)

        # add timestamp columns if they aren't part of the data items set (not used by any kpi)
        if self.eventTimestampName not in data_item_names:
            tableColumns.append("%s AS %s" % (
                dbhelper.quotingColumnName(self.eventTimestampColumn, self.is_postgre_sql),
                dbhelper.quotingColumnName(self.eventTimestampName, self.is_postgre_sql)))
            requested_col_names.append(self.eventTimestampName)

        # add all other data items used by KPIs
        for name in data_item_names:
            tableColumns.append("%s AS %s" % (
                dbhelper.quotingColumnName(self.data_items.get(name)[DATA_ITEM_COLUMN_NAME_KEY], self.is_postgre_sql),
                dbhelper.quotingColumnName(name, self.is_postgre_sql)))
            requested_col_names.append(name)

        # define where condition on all other data items to avoid rows that hold Nulls only. This can reduce the number of records to be retrieved.
        if len(data_item_names) > 0:
            where_not_null = ' OR '.join([('%s IS NOT NULL' % dbhelper.quotingColumnName(
                self.data_items.get(name)[DATA_ITEM_COLUMN_NAME_KEY], self.is_postgre_sql)) for name in data_item_names
                                          if (name != self.eventTimestampName and name != ENTITY_ID_NAME)])
            if len(where_not_null) > 0:
                where_not_null = 'AND ( %s ) ' % where_not_null
            else:
                where_not_null = None
        else:
            where_not_null = None

        if entities is None or len(util.asList(entities)) == 0:
            entities = [None]

        for entities_chunk in util.chunks(util.asList(entities), SQL_STATEMENT_ENTITIES_SIZE):
            if len(entities_chunk) == 1 and entities_chunk[0] is None:
                entities_chunk = None

            sql = "SELECT %s FROM %s.%s " % (
                ', '.join(tableColumns), dbhelper.quotingSchemaName(self.schema, self.is_postgre_sql),
                dbhelper.quotingTableName(self.eventTable, self.is_postgre_sql))
            sql += ("WHERE %s IS NOT NULL AND %s IS NOT NULL " % (
                dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql),
                dbhelper.quotingColumnName(self.eventTimestampColumn, self.is_postgre_sql)))

            if entities_chunk is not None:
                sql += ("AND %s IN (%s) " % (dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql),
                                             ','.join([dbhelper.quotingSqlString(chunk) for chunk in entities_chunk])))
            if start_ts is not None:
                sql += ("AND %s > %s " % (dbhelper.quotingColumnName(
                    self.eventTimestampColumn.lower() if self.is_postgre_sql else self.eventTimestampColumn,
                    self.is_postgre_sql), dbhelper.quotingSqlString(str(start_ts))))
            if end_ts is not None:
                sql += ("AND %s <= %s " % (dbhelper.quotingColumnName(
                    self.eventTimestampColumn.lower() if self.is_postgre_sql else self.eventTimestampColumn,
                    self.is_postgre_sql), dbhelper.quotingSqlString(str(end_ts))))
            if where_not_null is not None:
                sql += where_not_null
            sql += ("ORDER BY %s, %s ASC" % (dbhelper.quotingColumnName(self.entityIdName, self.is_postgre_sql),
                                             dbhelper.quotingColumnName(
                                                 self.eventTimestampName.lower() if self.is_postgre_sql else self.eventTimestampName,
                                                 self.is_postgre_sql)))

            df_chunks.append(self.db.read_sql_query(sql, requested_col_names=requested_col_names,
                                                    log_message='get_metric_data').fillna(np.nan))

        df = pd.concat(df_chunks, ignore_index=True, sort=False)

        # Cast types of columns that will be used for index. If timestamp is not explicitly given as type timestamp
        # but as integer we assume nanoseconds
        df = df.astype({self.entityIdName: str, self.eventTimestampName: 'datetime64[ns]'})

        self.logger.debug('get_metric_data: number of loaded records = %s, execution time = %s s' % (
            df.shape[0], (pd.Timestamp.utcnow() - start_time).total_seconds()))

        return df

    def get_derived_metric_data(self, data_item_names, timestamp=None, start_ts=None, end_ts=None, entities=None):
        # loading one key at a time since different keys could be of different data types,
        # also value columns need to be merged first and pivot_table would be required
        df_chunks = []
        for name in data_item_names:
            metadata = self.data_items.get(name)

            self.logger.debug('loading key=%s metadata=%s' % (name, str(metadata)))

            entities_chunk = entities
            sql = "SELECT * FROM %s.%s WHERE KEY = %s" % (
            dbhelper.quotingSchemaName(self.schema), dbhelper.quotingTableName(metadata.get(DATA_ITEM_SOURCETABLE_KEY)),
            dbhelper.quotingSqlString(name))
            if timestamp is not None:
                if start_ts is not None:
                    sql += " AND %s > %s" % (
                        dbhelper.quotingColumnName(timestamp), dbhelper.quotingSqlString(str(start_ts)))
                if end_ts is not None:
                    sql += " AND %s <= %s" % (
                        dbhelper.quotingColumnName(timestamp), dbhelper.quotingSqlString(str(end_ts)))
            if entities_chunk is not None:
                sql += " AND %s IN (%s) " % (dbhelper.quotingColumnName(KPI_ENTITY_ID_COLUMN), ','.join(
                    [dbhelper.quotingSqlString(chunk) for chunk in util.asList(entities_chunk)]))

            df_read = self.db.read_sql_query(sql, log_message='get_derived_metric_data')

            # we get all columns, so have to drop key column, unsed value columns, and last update column
            to_drop = list(TYPE_COLUMN_MAP.values())
            to_drop.remove(TYPE_COLUMN_MAP[metadata.get(DATA_ITEM_COLUMN_TYPE_KEY).upper()])
            to_drop.append('key')
            to_drop.append('last_update')
            df_read.drop(to_drop, axis=1, inplace=True, errors='ignore')

            log_data_frame('derived metric name=%s df read' % name, df_read.head())

            item_name_mappings = self.data_items.get_column_2_data_dict()
            item_name_mappings[TYPE_COLUMN_MAP[metadata.get(DATA_ITEM_COLUMN_TYPE_KEY).upper()]] = name
            self.patch_column_names(df_read, item_name_mappings)

            # move all granularity groupbase to index side for concatenation
            column_names = set(df_read.columns.values)
            column_names.discard(KPI_ENTITY_ID_COLUMN)
            column_names.discard(name)
            df_read = df_read.set_index(keys=[KPI_ENTITY_ID_COLUMN] + sorted(list(column_names)))

            log_data_frame('', df_read.head())

            df_chunks.append(df_read)

        df = pd.concat(df_chunks, axis=1, sort=False)

        # move all granularity groupbase back to column side
        df_read = df_read.reset_index(drop=True)

        return df

    def get_dimension_data(self, data_item_names, entities=None):
        requested_col_names = []
        tableColumns = list()

        # add entity id
        tableColumns.append("%s AS %s" % (dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql),
                                          dbhelper.quotingColumnName(self.entityIdName, self.is_postgre_sql)))
        requested_col_names.append(self.entityIdName)

        # add all other data items used by KPIs
        for name in data_item_names:
            tableColumns.append("%s AS %s" % (
                dbhelper.quotingColumnName(self.data_items.get(name)[DATA_ITEM_COLUMN_NAME_KEY], self.is_postgre_sql),
                dbhelper.quotingColumnName(name, self.is_postgre_sql)))
            requested_col_names.append(name)

        sql = "SELECT %s FROM %s.%s %s ORDER BY %s ASC" % (
            ', '.join(tableColumns), dbhelper.quotingSchemaName(self.schema, self.is_postgre_sql),
            dbhelper.quotingTableName(self.dimensionTable, self.is_postgre_sql),
            "" if entities is None else "WHERE %s IN (%s) " % (
                dbhelper.quotingColumnName(self.entityIdColumn, self.is_postgre_sql),
                ', '.join([dbhelper.quotingSqlString(ent) for ent in util.asList(entities)])),
            dbhelper.quotingColumnName(self.entityIdName, self.is_postgre_sql))
        self.logger.debug('get_dimension_sql=%s' % sql)

        df = self.db.read_sql_query(sql, requested_col_names=requested_col_names)

        df = df.astype({self.entityIdName: str})

        return df

    def patch_column_names(self, df, item_name_mappings):

        # SqlAlchemy connection to DB always returns column names in dataframe in lower case letters. Map returned
        # column names to data item names

        df_column_names = list(df.columns.values)
        new_df_column_names = [item_name_mappings.get(column, column) for column in df_column_names]

        self.logger.debug('df_column_names=%s, data_item_names=%s' % (df_column_names, new_df_column_names))

        df.columns = new_df_column_names

    def parse_kpi_dependency_tree(self, pipeline):
        """Generate the KPI dependency tree hierarchy with raw data items as level 0.

        This method create a treendoe per data item, and fill in the links between nodes
        according to the dependency relationship/hierarchy. Raw data items have level 0,
        derived metrics solely depend on raw items have level 1, so on and so forth. The
        level is determined by the max depth from a node to the root level (raw items).

        This method returns a list containing all treenodes, ordered by their level, from
        level 1 upward. The returned list can be used as a queue for processing the data
        items, taking dependency into consideration. It is guranteed that following the
        list sequence (by using list.pop(), that is lowest level at the end of the list)
        any dependency required by a data item would have already been processed.
        """
        raw_metrics_set = self.data_items.get_raw_metrics()
        derived_metrics_set = self.data_items.get_derived_metrics()

        processing_queue = list()

        kpi_tree = dict()

        # one function can have multiple outputs and it only needs to be invoked once to
        # generate all outputs. since we are creating one treenode per item, we can not
        # put all output items in the returned queue but just one of them, which
        # would avoid invoking the same instance multiple times. here we use a set to
        # store those names not to be put in the final queue
        sidecar_items = set()

        if len(self.pipeline_local) > 0:
            # if not in production mode, figure out any 'virtual' source/target not available
            # from metadata
            raw_metrics_set, derived_metrics_set = self.process_virtual_metrics(self.pipeline_local)

            virtual_raw_metrics_set = raw_metrics_set - self.data_items.get_raw_metrics()
            if len(virtual_raw_metrics_set) > 0:
                raise RuntimeError(
                    'unknown_raw_metrics=%s used in the pipeline, add them as data items to the system first' % str(
                        virtual_raw_metrics_set))

        self.logger.debug(
            'raw_metrics_set=%s, derived_metrics_set=%s' % (str(raw_metrics_set), str(derived_metrics_set)))

        for kpi in pipeline:
            name = get_kpi_targets(kpi)
            source = self.get_kpi_sources(kpi)

            # Check for cyclic dependency between input data items and output data items
            intersection = set(name) & source
            if len(intersection) > 0:
                msg = 'Incorrect cyclic definition of KPI function: The KPI function that is supposed to calculate '
                if len(intersection) > 1:
                    msg += 'the data items %s must not require these data items as input.' % intersection
                else:
                    msg += 'the data item \'%s\' must not require this data item as input.' % intersection.pop()
                raise Exception(msg)

            grain = set()
            if kpi.get(KPI_FUNCTION_GRANULARITY_KEY, None) is not None:
                grain = kpi[KPI_FUNCTION_GRANULARITY_KEY]
                grain = set(grain[1])

            raw_source_nodes = []
            source_nodes = []

            all_sources = (source | grain)
            raw_sources = all_sources & raw_metrics_set
            derived_sources = all_sources & derived_metrics_set
            missing_sources = all_sources - raw_sources - derived_sources

            if len(missing_sources) > 0:
                raise Exception(('The KPI function which calculates data item(s) %s requires ' + (
                    'data item %s as input but this data item has ' if len(
                        missing_sources) == 1 else 'data items %s as input but these data items have ') + 'not been defined neither as raw metric nor as derived metric nor as dimension.') % (
                                    name, list(missing_sources)))

            self.logger.debug('kpi_derived_metrics = %s, kpi_raw_sources=%s, kpi_derived_sources=%s, kpi=%s' % (
                str(name), str(raw_sources), str(derived_sources), str(kpi)))

            # 1st pass can only create nodes for raw sources
            for s in raw_sources:
                tn = KpiTreeNode(name=s, kpi=None, dependency=None, level=0)
                kpi_tree[s] = tn
                raw_source_nodes.append(tn)
                source_nodes.append(tn)

            # for derived ones, simply insert their names first
            source_nodes.extend(derived_sources)

            # for each target, create a treenode with all source nodes as dependency
            for idx, n in enumerate(name):
                kpi_tree[n] = KpiTreeNode(name=n, kpi=kpi, dependency=source_nodes)
                if idx > 0:
                    sidecar_items.add(n)

            if len(name) == 0 and len(source) == 0:
                # it has neither input nor output (data items), put it up front always
                processing_queue.append(
                    KpiTreeNode(name='%s_%s' % (kpi[KPI_FUNCTION_FUNCTIONNAME_KEY], util.randomword(8)), kpi=kpi,
                                dependency=[]))

        # 2nd pass to replace any string source reference with KpiTreeNode source (could only be derived metrics)
        all_aggregators = self.catalog.get_aggregators()
        for k, v in kpi_tree.items():
            if v.dependency is not None:
                for idx, dep in enumerate(v.dependency):
                    if not isinstance(dep, KpiTreeNode):
                        v.dependency[idx] = kpi_tree[dep]
                        kpi_tree[dep].children.add(v)

        for k, v in kpi_tree.items():
            # normally, server side KPI definition takes care of inherited granularity, that is, for
            # transformation or aggregation depending on other kpis, the parent's granularity is
            # checked and the correct granularity is always set for all KPIs
            # but when in client mode, for the 'virtual' kpis, there's no such checking done on the
            # client side, we have to check with another pass for all KPIs without granularity, and
            # for them if any of its parent does have granularity, we set it to be same as its parent
            if v.kpi is not None and v.kpi[KPI_FUNCTION_FUNCTIONNAME_KEY] not in all_aggregators and v.kpi.get(
                    KPI_FUNCTION_GRANULARITY_KEY) is None:
                self.logger.warning('found transformer without granularity: %s' % v.name)

                queue = list()
                queue.extend(v.dependency)
                while len(queue) > 0:
                    dep = queue.pop()
                    if dep.dependency is not None and len(dep.dependency) > 0:
                        for dp in dep.dependency:
                            queue.insert(0, dp)

                    if dep.name in self.target_grains:
                        # set target's grain correctly as well
                        self.target_grains[v.name] = self.target_grains[dep.name]
                        # set it to be the same as its parent
                        v.kpi[KPI_FUNCTION_GRANULARITY_KEY] = self.target_grains[dep.name]
                        # we assume all dependencies must have the same granularity
                        self.logger.debug('granularity=%s' % str(v.kpi[KPI_FUNCTION_GRANULARITY_KEY]))
                        break
                    elif dep.name in self.target_grains_local:
                        # set target's grain correctly as well
                        self.target_grains_local[v.name] = self.target_grains_local[dep.name]
                        # set it to be the same as its parent
                        v.kpi[KPI_FUNCTION_GRANULARITY_KEY] = self.target_grains_local[dep.name]
                        # we assume all dependencies must have the same granularity
                        self.logger.debug('granularity=%s' % str(v.kpi[KPI_FUNCTION_GRANULARITY_KEY]))
                        break

        self.validate_tree(kpi_tree)

        return (kpi_tree, sidecar_items, processing_queue)

    def get_kpi_dependency_tree_processing_queue(self, pipeline):
        kpi_tree, sidecar_items, processing_queue = self.parse_kpi_dependency_tree(pipeline=pipeline)

        # fill all level 1 into the queue (level 0, raw ones do not need to be inserted)
        leveled_items = defaultdict(list)
        for name, tn in kpi_tree.items():
            # self.logger.debug('last pass data item: ' + str(tn))
            if tn.tree_level() == 1 and tn.name not in sidecar_items:
                processing_queue.append(tn)
            elif tn.tree_level() > 1:
                leveled_items[tn.tree_level()].append(tn)

        # now push those with level > 1, in the order of level (2, 3, 4, etc...)
        for level in sorted(leveled_items.keys()):
            for tn in leveled_items[level]:
                if tn.name not in sidecar_items:
                    processing_queue.append(tn)

        if self.logger.isEnabledFor(logging.DEBUG):
            queue_debug_string = 'kpi_dependencies = '
            for q in processing_queue:
                queue_debug_string += '\n    %s' % q
            self.logger.debug(queue_debug_string)

        return processing_queue

    def process_virtual_metrics(self, pipeline):
        """Process any virtual metric contained in the given pipeline.

        When in client mode, local pipeline could contain metrics that are defined on server side yet,
        raw or derived. This method parse the given pipeline to find out all such metrics, based on
        the server side data item definition. It also checks any virtual item used in granularity sets.

        This method returns a tuple of two sets, the first being the raw metrics and the second being
        the derived metrics. Note that both sets contain all metrics, server side defined and virtual
        ones, but it never touches the actual cached copy of server side data items. The returned sets
        are simply copies.
        """
        raw_metrics_set = self.data_items.get_raw_metrics().copy()
        derived_metrics_set = self.data_items.get_derived_metrics().copy()

        for kpi in pipeline:
            # find any 'virtual' target
            for name in get_kpi_targets(kpi):
                if name in derived_metrics_set:
                    raise RuntimeError('duplicate output_data_item=%s defined in multiple kpi functions' % name)

                derived_metrics_set.add(name)
                self.logger.debug('non-production mode added derived_metric=%s' % name)
        for kpi in pipeline:
            # find any 'virtual' source
            for name in self.get_kpi_sources(kpi):
                if name not in derived_metrics_set and name not in raw_metrics_set and re.fullmatch(r'[0-9a-zA-Z-_]+',
                                                                                                    name) is not None:
                    raw_metrics_set.add(name)
                    self.logger.debug('non-production mode added source_metric=%s' % name)

            # find any 'virtual' raw dimension which is used in granularity but not source
            if kpi.get(KPI_FUNCTION_GRANULARITY_KEY, None) is not None:
                grain = kpi[KPI_FUNCTION_GRANULARITY_KEY]
                for gd in set(grain[1]):
                    if gd not in derived_metrics_set and gd not in raw_metrics_set:
                        raw_metrics_set.add(gd)
                        self.logger.debug('non-production mode added granularity_dimension=%s' % gd)

        return (raw_metrics_set, derived_metrics_set)

    def validate_tree(self, kpi_tree):
        """Validate the tree and remove any invalid node along with all of its descendents."""
        removed = set()
        for name, node in kpi_tree.items():
            kpi = node.kpi
            if kpi is None:
                # raw metric
                continue

            catalog_function = self.catalog.get_function(kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY))
            if catalog_function is None:
                # remove this node and all its descendents
                removed.add(name)
                removed.update({n.name for n in node.get_all_descendants()})

        for name in removed:
            kpi_tree.pop(name, None)

        return removed

    def generate_pipeline_stages(self, pipeline, start_ts):
        """Generate pipeline stages based on the given KPI configuration.

        The given config contains a dict of KPIs, keyed by function with value of a list of KPIs.
        This method bases on those KPIs, taken into consideration the dependency hierarchy among
        KPIs, to create a staged pipeline. Each stage represents one function typically.

        The reason to group by function is to have a chance to pack multiple calls to the same
        function. Aggregation fits this as we want to do one groupby while applying as many agg
        functions as possible. Same applies to transformer as it reduces the dataframe
        manipulation overhead.
        """

        all_stages = []
        persist_cols = []
        function_kpi_generated = []

        loaders = self.catalog.get_loaders()
        alerts = self.catalog.get_alerts()
        transformers = self.catalog.get_transformers()
        all_aggregators = self.catalog.get_aggregators()

        grouped_aggregators = defaultdict(list)

        for kpi in pipeline:
            fname = kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY)

            if fname in transformers:
                if fname in loaders:
                    # skip all loaders, they are specially processed before any stage
                    continue

                inputParams = kpi.get(KPI_FUNCTION_INPUT_KEY)
                outputParams = kpi.get(KPI_FUNCTION_OUTPUT_KEY)

                params_dict = {}
                for key in inputParams:
                    params_dict[key] = inputParams[key]
                for key in outputParams:
                    params_dict[key] = outputParams[key]

                # self.logger.info('function_name=%s, kpi_function=%s, function_params_dict=%s' % (fname, str(kpi), str(params_dict)))

                try:
                    logger.info('Initializing Transformation function %s' % fname)
                    func_object = transformers[fname](**params_dict)
                    func_object.scope = kpi.get(KPI_FUNCTION_SCOPE_KEY)
                    # Update list of output parameters
                    if not getattr(func_object, '_outputs', None):
                        func_object._outputs = outputParams.values()
                    if getattr(func_object, '_get_dms', None) and getattr(func_object, '_set_dms', None):
                        func_object._set_dms(self)
                    all_stages.append(func_object)
                except Exception as e:
                    msg = 'Error while initializing function %s with parameter (%s) ' % (fname, str(params_dict))
                    self.entity_type_obj.raise_error(exception=e, msg=msg, abort_on_fail=True,
                                                     stage_name="Initialize functions")

                kpi_targets = get_kpi_targets(kpi)
                persist_cols.extend(kpi_targets)

                function_kpi_generated.append(
                    (fname, kpi.get(KPI_FUNCTION_NAME_KEY), kpi_targets, kpi.get(KPI_FUNCTION_FUNCTION_ID_KEY)))
            elif fname in all_aggregators:
                # for aggregators, it is safe to group same function together, unlike transformers
                grouped_aggregators[fname].append(kpi)

        granularity = None
        simple_aggregators = list()
        complex_aggregators = list()
        direct_aggregators = list()

        # now deal with grouped aggregators
        for fname, fname_kpis in grouped_aggregators.items():
            for kpi in fname_kpis:
                # it is assumed that only the same 'grain' would end up here together, so any one
                # can be used, they are all the same
                granularity = kpi.get(KPI_FUNCTION_GRANULARITY_KEY)

                inputParams = kpi.get(KPI_FUNCTION_INPUT_KEY)
                outputParams = kpi.get(KPI_FUNCTION_OUTPUT_KEY)

                # for now, aggregators can only have one source and one name, though input can have
                # more params other than source

                func = all_aggregators[fname]

                func._entity_type = self.entity_type_obj

                if inspect.isclass(func) and 'is_direct_aggregator' in dir(func) and func.is_direct_aggregator:
                    # direct aggregator, instantiate it with all inputs and use its 'execute' method as func
                    params_dict = {}
                    for key in inputParams:
                        params_dict[key] = inputParams[key]
                    for key in outputParams:
                        params_dict[key] = outputParams[key]
                    func = getattr(func(**params_dict), 'execute')
                    direct_aggregators.append((self.get_kpi_sources(kpi), func, get_kpi_targets(kpi)))
                elif inspect.isclass(func) and (
                        'is_complex_aggregator' in dir(func) and func.is_complex_aggregator or issubclass(func,
                                                                                                          aggregate.ComplexAggregator)):
                    # complex aggregator, instantiate it with all inputs and use its 'execute' method as func
                    params_dict = {}
                    for key in inputParams:
                        params_dict[key] = inputParams[key]
                    for key in outputParams:
                        params_dict[key] = outputParams[key]
                    func = getattr(func(**params_dict), 'execute')
                    complex_aggregators.append((self.get_kpi_sources(kpi), func, get_kpi_targets(kpi)))
                else:
                    if inspect.isclass(func) and (
                            'is_simple_aggregator' in dir(func) and func.is_simple_aggregator or issubclass(func,
                                                                                                            aggregate.SimpleAggregator)):
                        # simple aggregator, instantiate it with all inputs except source and use its 'execute' method as func
                        params_dict = {inKey: params for inKey, params in inputParams.items() if
                                       inKey != AGGREGATOR_INPUT_SOURCE_KEY}
                        func_name = 'execute_%s' % fname.lower()
                        # because groupby.agg does not allow duplicate method name, we have to rename 'execute' even from different class
                        add_simple_aggregator_execute(func, func_name)
                        func = getattr(func(**params_dict), func_name)
                    elif inspect.isfunction(func):
                        func = partial(func)

                    simple_aggregators.append(
                        (inputParams[AGGREGATOR_INPUT_SOURCE_KEY], func, outputParams[AGGREGATOR_OUTPUT_SOURCE_KEY]))

                function_kpi_generated.append((
                    fname, kpi.get(KPI_FUNCTION_NAME_KEY), [outputParams[AGGREGATOR_OUTPUT_SOURCE_KEY]],
                    kpi.get(KPI_FUNCTION_FUNCTION_ID_KEY)))

        new_sources = [util.asList(sa[0]) for sa in simple_aggregators]
        new_names = [util.asList(sa[2]) for sa in simple_aggregators]
        for ca in complex_aggregators:
            new_sources.extend(ca[0])
            new_names.extend(ca[2])
        for da in direct_aggregators:
            new_sources.extend(da[0])
            new_names.extend(da[2])

        # # flatten the lists of aggregator sources and names since individual element can be a list of strings
        new_sources_temp = []
        for element in new_sources:
            if isinstance(element, str):
                new_sources_temp.append(element)
            elif isinstance(element, list) and all([isinstance(e, str) for e in element]):
                new_sources_temp.extend(element)
        new_sources = new_sources_temp
        new_names_temp = []
        for element in new_names:
            if isinstance(element, str):
                new_names_temp.append(element)
            elif isinstance(element, list) and all([isinstance(e, str) for e in element]):
                new_names_temp.extend(element)
        new_names = new_names_temp

        self.logger.debug('new_sources=%s, new_names=%s' % (new_sources, new_names))

        # if len(new_sources) == 0:
        if len(simple_aggregators) == 0 and len(complex_aggregators) == 0 and len(direct_aggregators) == 0:
            # projected_columns = list(self.data_items.get_raw_metrics())
            # all_stages.insert(0, ProjectColumns(sources=projected_columns))
            # TODO figure out the right source set from kpis
            pass
        else:
            projected_columns = list(set(new_sources)) + [self.eventTimestampName] + list(granularity[1])
            all_stages.insert(0, ProjectColumns(sources=projected_columns))
            all_stages.insert(1, Aggregation(dms=self, ids=self.entityIdName if granularity[2] else None,
                                             timestamp=self.eventTimestampName if granularity[0] is not None else None,
                                             granularity=granularity, simple_aggregators=simple_aggregators,
                                             complex_aggregators=complex_aggregators,
                                             direct_aggregators=direct_aggregators))
            # all_stages.insert(2, AggregationIncrementalUpdate(self, names=new_names, aggregators=new_aggregatos, timestamp=self.eventTimestampName, granularity=granularity))
            persist_cols.extend(new_names)

        all_persist_cols = []
        for col in persist_cols:
            if isinstance(col, list):
                all_persist_cols.extend(col)
            else:
                all_persist_cols.append(col)

        all_stages.append(PersistColumns(self, sources=list(set(all_persist_cols))))

        all_stages.append(ProduceAlerts(self, all_cols=list(set(all_persist_cols))))

        # record usage data
        # all_stages.append(RecordUsage(dms=self, function_kpi_generated=function_kpi_generated, start_ts=start_ts, completed=True))

        self.logger.debug('pipeline_stages=%s' % str([stage.__class__.__name__ for stage in all_stages]))

        return all_stages

    def generate_loader_stage(self, pipeline):

        all_stages = []
        function_kpi_generated = []

        loaders = self.catalog.get_loaders()

        for kpi in pipeline:
            fname = kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY)
            if fname not in loaders:
                continue

            func = loaders[fname]

            inputParams = kpi.get(KPI_FUNCTION_INPUT_KEY)
            outputParams = kpi.get(KPI_FUNCTION_OUTPUT_KEY)

            params_dict = {}
            for key in inputParams:
                params_dict[key] = inputParams[key]
            for key in outputParams:
                params_dict[key] = outputParams[key]

            self.logger.info(
                'function_name=%s, kpi_function=%s, function_params_dict=%s' % (fname, str(kpi), str(params_dict)))

            try:
                func_object = func(**params_dict)
                if getattr(func_object, '_get_dms', None) and getattr(func_object, '_set_dms', None):
                    func_object._set_dms(self)
                all_stages.append(func_object)
            except Exception:
                self.logger.warning(
                    'Error while initializing function %s with parameter (%s) ' % (fname, str(params_dict)),
                    exc_info=True)

            kpi_targets = get_kpi_targets(kpi)

            function_kpi_generated.append(
                (fname, kpi.get(KPI_FUNCTION_NAME_KEY), kpi_targets, kpi.get(KPI_FUNCTION_FUNCTION_ID_KEY)))

        if len(all_stages) == 0:
            return None

        # record usage data
        # all_stages.append(RecordUsage(dms=self, function_kpi_generated=function_kpi_generated, start_ts=self.launch_date, completed=True))

        self.logger.debug('pipeline_stages=%s' % str([stage.__class__.__name__ for stage in all_stages]))

        return loader.LoaderPipeline(all_stages, self.dblogging)

    def get_cache_filename(self, dep_grain, grain):
        """Get the cache file local path.

        This method first composes the cache file name, then tries to download it from COS
        and put it at the right path, then returns the local path. If for whatever reason
        the COS download fails, it removes the local copy at the path.
        """
        base_path = '%s/%s/%s' % (PARQUET_DIRECTORY, self.tenant_id, self.entity_type)
        Path(base_path).mkdir(parents=True, exist_ok=True)

        src = '%s_%s_%s' % (
            str(dep_grain[0]), str('_'.join(dep_grain[1])), str(dep_grain[2])) if dep_grain is not None else str(None)
        tar = '%s_%s_%s' % (str(grain[0]), str('_'.join(grain[1])), str(grain[2])) if grain is not None else str(None)
        local_path = '%s/df_parquet__%s__%s' % (base_path, src, tar)

        content = cos.cos_get(local_path, bucket=COS_BUCKET_KPI, binary=True)
        if content is not None:
            # save the downloaded content locally
            Path(local_path).write_bytes(content)

        if content is None:
            # nonexistent yet, make sure there's no local copy
            try:
                os.remove(local_path)
            except OSError:
                pass

        return local_path

    def clean_cache_files(self):
        if self.production_mode:
            path = '%s/%s/%s/df_parquet__' % (PARQUET_DIRECTORY, self.tenant_id, self.entity_type)
            cos.cos_delete_multiple(cos.cos_find(path, bucket=COS_BUCKET_KPI), bucket=COS_BUCKET_KPI)

    def get_kpi_sources(self, kpi):
        catalog_function = self.catalog.get_function(kpi.get(KPI_FUNCTION_FUNCTIONNAME_KEY))
        if catalog_function is not None and catalog_function.get(KPI_FUNCTION_INPUT_KEY) is not None:

            sources = get_fn_expression_args(catalog_function, kpi)

            data_item_input_params = {input.get(FUNCTION_PARAM_NAME_KEY) for input in
                                      catalog_function.get(KPI_FUNCTION_INPUT_KEY, []) if
                                      input.get(FUNCTION_PARAM_TYPE_KEY) == 'DATA_ITEM'}

            for key in data_item_input_params:
                if len(kpi[KPI_FUNCTION_INPUT_KEY]) == 0:
                    logger.warning("Kpi input is empty. Please check the configuration: %s" % (
                        str(kpi)))  # TODO: Check if input is mandatory. If input is mandatory then throw an exception.
                else:
                    values = kpi[KPI_FUNCTION_INPUT_KEY][key]

                    # input of type DATA_ITEM must be a string or a list of string

                    if isinstance(values, str):
                        values = [values]
                    elif not isinstance(values, list):
                        logger.warning('data_item_input=(%s: %s) is neither a string nor a list, kpie=%s' % (
                            key, str(values), str(kpi)))
                        continue
                    elif any([not isinstance(src, str) for src in values]):
                        logger.warning(
                            'data_item_input=(%s: %s) is a list but not all its elements are string, kpie=%s' % (
                                key, str(values), str(kpi)))
                        continue

                    sources.update(set(values))

            sources.update(get_fn_scope_sources(KPI_FUNCTION_SCOPE_KEY, kpi))

        else:

            sources = set()

        return sources

    def get_all_kpi_sources(self, pipeline):
        sources = set()

        for kpi in pipeline:
            sources.update(self.get_kpi_sources(kpi))

        return sources


def get_kpi_targets(kpi):
    targets = list()

    for key in kpi.get(KPI_FUNCTION_OUTPUT_KEY, []):
        target = kpi[KPI_FUNCTION_OUTPUT_KEY][key]
        if isinstance(target, str):
            # targets.append(target)
            targets.extend([t.strip() for t in target.split(',') if len(t.strip()) > 0])
        elif isinstance(target, list) and all([isinstance(t, str) for t in target]):
            targets.extend(target)

    return targets


def get_all_kpi_targets(pipeline):
    targets = set()

    for kpi in pipeline:
        targets.update(get_kpi_targets(kpi))

    return targets


def get_all_granularity_dimensions(pipeline, granularities):
    granularity_dimensions = set()

    for kpi in pipeline:
        if kpi.get(KPI_FUNCTION_GRANULARITY_KEY) is not None:
            # gran = granularities[kpi[KPI_FUNCTION_GRANULARITY_KEY]]
            # granularity_dimensions.update(gran[1])
            granularity_dimensions.update(kpi[KPI_FUNCTION_GRANULARITY_KEY][1])

    return granularity_dimensions


def add_simple_aggregator_execute(cls, func_name):
    def fn(self, group):
        return self.execute(group)

    setattr(cls, func_name, fn)
    fn.__name__ = func_name


class AnalyticsServiceResult(defaultdict):

    def __init__(self, granularities):
        self.granularities = granularities

    def get_granularity(self, grain_name):
        if grain_name is None:
            return self.get(None)
        elif grain_name not in self.granularities:
            return None

        return self.get(self.granularities[grain_name])


class CheckpointsHelper:

    def __init__(self, df_checkpoints, df_updated_entities, df_updated_stale_entities, df_new_entities, db_type):
        self.df_checkpoints = df_checkpoints
        self.df_updated_entities = df_updated_entities
        self.df_updated_stale_entities = df_updated_stale_entities
        self.df_new_entities = df_new_entities
        self.db_type = db_type

    def get_checkpoints(self):
        return self.df_checkpoints

    def has_no_updated_entities(self):
        return self.df_updated_entities.empty

    def has_no_updated_stale_entities(self):
        return self.df_updated_stale_entities.empty

    def has_no_new_entities(self):
        return self.df_new_entities.empty

    def get_common_start_for_updated_entities(self):
        start_timestamp = self.df_updated_entities['last_timestamp'].min()
        return None if pd.isna(start_timestamp) else str(start_timestamp)

    def get_common_start_for_updated_stale_entities(self):
        start_timestamp = self.df_updated_stale_entities['last_timestamp'].min()
        return None if pd.isna(start_timestamp) else str(start_timestamp)

    def get_updated_entities(self):
        return self.df_updated_entities[KPI_ENTITY_ID_COLUMN].unique().tolist()

    def get_updated_stale_entities(self):
        return self.df_updated_stale_entities[KPI_ENTITY_ID_COLUMN].unique().tolist()

    def get_new_entities(self):
        return self.df_new_entities[KPI_ENTITY_ID_COLUMN].unique().tolist()


class DataItemMetadata():

    def __init__(self):
        self.data_items = dict()

    def add(self, data_item):
        self.data_items[data_item[DATA_ITEM_NAME_KEY]] = data_item

    def get_all_names(self):
        return {v[DATA_ITEM_NAME_KEY] for v in self.data_items.values()}

    def get(self, name):
        return self.data_items.get(name, None)

    def get_names(self, type):
        return {v[DATA_ITEM_NAME_KEY] for v in self.data_items.values() if v[DATA_ITEM_TYPE_KEY] in util.asList(type)}

    def get_column_2_data_dict(self):
        return {v['columnName'].lower(): k for k, v in self.data_items.items()}

    def get_dimensions(self):
        return self.get_names([DATA_ITEM_TYPE_DIMENSION])

    def get_raw_metrics(self):
        return self.get_names([DATA_ITEM_TYPE_METRIC, DATA_ITEM_TYPE_EVENT, DATA_ITEM_TYPE_DIMENSION])

    def get_derived_metrics(self):
        return self.get_all_names() - self.get_raw_metrics()


class ProjectColumns:

    def __init__(self, sources=None):
        self.logger = logging.getLogger('%s.%s' % (self.__module__, self.__class__.__name__))

        if sources is None:
            raise RuntimeError("argument sources must be provided")
        self.sources = util.asList(sources)

    def execute(self, df):
        cols = [x for x in df.columns if x in self.sources]
        self.logger.debug('projected_columns=%s, projected_columns_sources=%s' % (str(cols), str(self.sources)))
        df = df[cols]
        return df


class KpiTreeNode(object):
    def __init__(self, name, kpi, dependency=None, level=None):
        self.name = name
        self.kpi = kpi
        if dependency is None or isinstance(dependency, list):
            self.dependency = dependency
        else:
            self.dependency = [dependency]
        self._level = level
        self.children = set()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def tree_level(self):
        if self._level is not None or self.dependency is None:
            return self._level
        elif self.dependency and len(self.dependency) > 0:
            return max([d.tree_level() if isinstance(d, KpiTreeNode) else 0 for d in self.dependency]) + 1
        else:
            return 1

    def __repr__(self):
        if self.dependency is not None:
            return '(%s) %s <- %s' % (
            self.tree_level(), self.name, str(['(%s) %s' % (dep.tree_level(), dep.name) for dep in self.dependency]))
        else:
            return '%s' % (self.name)

    def get_all_dependencies(self):
        dependencies = set()

        if self.dependency is None:
            return dependencies

        queue = self.dependency.copy()
        while len(queue) > 0:
            treenode = queue.pop(0)
            dependencies.add(treenode)
            if treenode.dependency is not None and len(treenode.dependency) > 0:
                queue.extend(treenode.dependency)

        return dependencies

    def get_all_descendants(self):
        descendants = set()
        queue = list(self.children)
        while len(queue) > 0:
            treenode = queue.pop(0)
            descendants.add(treenode)
            if len(treenode.children) > 0:
                queue.extend(treenode.children)

        return descendants


class Aggregation:

    def __init__(self, dms, ids=None, timestamp=None, granularity=None, simple_aggregators=None,
                 complex_aggregators=None, direct_aggregators=None):
        """
        Keyword arguments:
        ids -- the names of entity id columns, can be a string or a list of
               string. aggregation is always done first by entities unless
               this is not given (None) and it is not allowed to include any
               of entity id columns in sources
        """
        self.logger = logging.getLogger('%s.%s' % (self.__module__, self.__class__.__name__))

        self.dms = dms

        if simple_aggregators is None:
            simple_aggregators = []

        if complex_aggregators is None:
            complex_aggregators = []

        if direct_aggregators is None:
            direct_aggregators = []

        self.simple_aggregators = simple_aggregators
        self.complex_aggregators = complex_aggregators
        self.direct_aggregators = direct_aggregators

        self.ids = ids
        if self.ids is not None:
            # if not set(self.ids).isdisjoint(set([sa[0] for sa in self.simple_aggregators])):
            #     raise RuntimeError('sources (%s) must not include any columns in ids (%s), use grain entityFirst attribute to have that' % (str(self.sources), str(self.ids)))
            self.ids = util.asList(self.ids)
        else:
            self.ids = list()

        self.timestamp = timestamp

        self.logger.debug('aggregation_input_granularity=%s' % str(granularity))

        if granularity is not None and not isinstance(granularity, tuple):
            raise RuntimeError('argument granularity must be a tuple')

        self.frequency = None
        self.groupby = None
        self.entityFirst = True
        if granularity is not None:
            self.frequency, self.groupby, self.entityFirst, dummy = granularity

        if self.groupby is None:
            self.groupby = ()

        if self.groupby is not None and not isinstance(self.groupby, tuple):
            raise RuntimeError('argument granularity[1] must be a tuple')

        self.logger.debug(
            'aggregation_ids=%s, aggregation_timestamp=%s, aggregation_simple_aggregators=%s, aggregation_complex_aggregators=%s, aggregation_direct_aggregators=%s, aggregation_frequency=%s, aggregation_groupby=%s, aggregation_entityFirst=%s' % (
                str(self.ids), str(self.timestamp), str(self.simple_aggregators), str(self.complex_aggregators),
                str(self.direct_aggregators), str(self.frequency), str(self.groupby), str(self.entityFirst)))

    def _agg_dict(self, df, simple_aggregators):
        numerics = df.select_dtypes(include=[np.number, bool]).columns.values

        agg_dict = defaultdict(list)
        for srcs, agg, name in simple_aggregators:
            srcs = util.asList(srcs)
            for src in srcs:
                if src in numerics:
                    agg_dict[src].append(agg)
                else:
                    numeric_only_funcs = set(['sum', 'mean', 'std', 'var', 'prod', aggregate.Sum, aggregate.Mean,
                                              aggregate.StandardDeviation, aggregate.Variance, aggregate.Product])
                    if agg not in numeric_only_funcs:
                        agg_dict[src].append(agg)

        return agg_dict

    def execute(self, df):
        agg_dict = self._agg_dict(df, self.simple_aggregators)

        self.logger.debug('aggregation_column_methods=%s' % dict(agg_dict))

        df = df.reset_index()

        group_base = []
        if len(self.ids) > 0 and self.entityFirst:
            group_base.extend(self.ids)

        if self.timestamp is not None and self.frequency is not None:
            if self.frequency == 'W':
                # 'W' by default use right label and right closed
                group_base.append(pd.Grouper(key=self.timestamp, freq=self.frequency, label='left', closed='left'))
            else:
                # other alias seems to not needing to special handle
                group_base.append(pd.Grouper(key=self.timestamp, freq=self.frequency))

        if self.groupby is not None and len(self.groupby) > 0:
            group_base.extend(self.groupby)

        self.logger.debug('aggregation_groupbase=%s' % str(group_base))

        groups = df.groupby(group_base)

        all_dfs = []

        # simple aggregators

        df_agg = groups.agg(agg_dict)

        log_data_frame('aggregation_after_groupby_df_agg', df_agg.head())

        renamed_cols = {}
        for srcs, agg, names in self.simple_aggregators:
            for src, name in zip(util.asList(srcs), util.asList(names)):
                func_name = agg.func.__name__ if hasattr(agg, 'func') else agg.__name__ if hasattr(agg,
                                                                                                   '__name__') else agg
                renamed_cols['%s|%s' % (src, func_name)] = name if name is not None else src
        for name in (
                set(agg_dict.keys()) - set([item for sa in self.simple_aggregators for item in util.asList(sa[0])])):
            for agg in agg_dict[name]:
                func_name = agg.func.__name__ if hasattr(agg, 'func') else agg.__name__ if hasattr(agg,
                                                                                                   '__name__') else agg
                renamed_cols['%s|%s' % (name, func_name)] = name

        self.logger.info('after simple aggregation function - sources %s' % str(renamed_cols))

        new_columns = []
        for col in df_agg.columns:
            if len(col[-1]) == 0 or col[0] in ([self.timestamp] + list(self.groupby)):
                new_columns.append('|'.join(col[:-1]))
            else:
                new_columns.append('|'.join(col))
        df_agg.columns = new_columns

        if len(renamed_cols) > 0:
            df_agg.rename(columns=renamed_cols, inplace=True)

        all_dfs.append(df_agg)

        log_data_frame('aggregation_df_agg', df_agg.head())

        # complex aggregators

        for srcs, func, names in self.complex_aggregators:

            self.logger.info('executing complex aggregation function - sources %s' % str(srcs))
            self.logger.info('executing complex aggregation function - output %s' % str(names))
            df_apply = groups.apply(func)

            if df_apply.empty and df_apply.columns.empty:
                for name in names:
                    df_apply[name] = None

                    source_metadata = self.dms.data_items.get(name)
                    if source_metadata is None:
                        continue

                    if source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_NUMBER:
                        df_apply = df_apply.astype({name: float})
                    elif source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_BOOLEAN:
                        df_apply = df_apply.astype({name: bool})
                    elif source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_TIMESTAMP:
                        df_apply = df_apply.astype({name: 'datetime64[ns]'})
                    else:
                        df_apply = df_apply.astype({name: str})

            all_dfs.append(df_apply)

            log_data_frame('func=%s, aggregation_df_apply' % str(func), df_apply.head())

        # direct aggregators

        for srcs, func, names in self.direct_aggregators:

            self.logger.info('executing direct aggregation function - sources %s' % str(srcs))
            self.logger.info('executing direct aggregation function - output %s' % str(names))

            df_direct = func(df=df, group_base=group_base)
            if df_direct.empty and df_direct.columns.empty:
                for name in names:
                    df_direct[name] = None

                    source_metadata = self.dms.data_items.get(name)
                    if source_metadata is None:
                        continue

                    if source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_NUMBER:
                        df_direct = df_direct.astype({name: float})
                    elif source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_BOOLEAN:
                        df_direct = df_direct.astype({name: bool})
                    elif source_metadata.get(DATA_ITEM_COLUMN_TYPE_KEY) == DATA_ITEM_DATATYPE_TIMESTAMP:
                        df_direct = df_direct.astype({name: 'datetime64[ns]'})
                    else:
                        df_direct = df_direct.astype({name: str})

            all_dfs.append(df_direct)

            log_data_frame('func=%s, aggregation_df_direct' % str(func), df_direct.head())

        # concat all results
        df = pd.concat(all_dfs, axis=1)

        log_data_frame('aggregation_final_df', df.head())

        return df


class AggregationReloadUpdate:
    """This class supports incremental update of aggregation by reloading cached input raw data.

    Before entering an aggregation level, this class is called first. What it does is simply caching
    its output before passing to the next, the actual aggregation level. Its input, raw data, is
    also concatenated with the cached data before passing on. Before concatenating, it checks the
    range of its input data and use that to 'evict' the cached data in order to keep it fresh.

    One significant assumption here is that input data is always 'increasing' in time. This class
    cannot handle input data far 'back in time'.
    """

    def __init__(self, dms, timestamp, granularity, cache, concat_only, production_mode):
        self.logger = logging.getLogger('%s.%s' % (self.__module__, self.__class__.__name__))

        if dms is None:
            raise RuntimeError('argument dms must be provided')
        if granularity is None or not isinstance(granularity, tuple):
            raise RuntimeError('argument granularity must be given and must be a tuple')
        if concat_only is None:
            raise RuntimeError('argument concat_only must be given and must be a boolean')

        self.dms = dms
        self.timestamp = timestamp
        self.granularity = granularity

        self.frequency = None
        self.groupby = None
        self.entityFirst = True
        if granularity is not None:
            self.frequency, self.groupby, self.entityFirst, dummy = granularity

        if self.groupby is None:
            self.groupby = ()

        if self.groupby is not None and not isinstance(self.groupby, tuple):
            raise RuntimeError('argument granularity[1] must be a tuple')

        if self.timestamp is None and self.frequency is not None:
            raise RuntimeError('argument timestamp must be given when time-based granularity is used')

        self.concat_only = concat_only
        self.df_cache = cache
        self.production_mode = production_mode

        self.logger.debug(
            'aggregation_reload_timestamp=%s, aggregation_reload_frequency=%s, aggregation_reload_groupby=%s, aggregation_reload_entityFirst=%s, aggregation_reload_concat_only=%s' % (
                str(self.timestamp), str(self.frequency), str(self.groupby), str(self.entityFirst),
                str(self.concat_only)))

    def execute(self, df, dep_grain, grain):
        # any NA groupby column rows are skipped in anyway
        df.dropna(how='any', subset=list(set(self.groupby) & set(df.columns)), inplace=True)
        log_data_frame('aggregation_reload_df', df.head())

        if df.empty:
            return df

        if self.dms.running_with_backtrack is False:
            # Handle cache file and load data from cache file in to dataframe

            # load back the cached dataframe
            df_loaded_from_cache = None
            remove_old_cache = False

            if self.dms.ignore_cache is False:

                df_loaded_from_cache = self.df_cache.retrieve_cache(dep_grain, grain)

                # Migration from old parquet filename to new parquet filename
                if df_loaded_from_cache is None:
                    # Try to find cache file with old name
                    df_loaded_from_cache = self.df_cache.retrieve_cache(dep_grain, grain, old_name=True)
                    if df_loaded_from_cache is not None:
                        remove_old_cache = True
            else:
                self.logger.info('Cache file is ignored because check points cannot be used in current mode. ' \
                                 'No cached data are loaded from cache file into dataframe.')

            if df_loaded_from_cache is not None and not df_loaded_from_cache.empty:
                timestamp_dimension_used = None
                if self.frequency is None:
                    # it is assume either time frequency is used or a timestamp-typed dimension is used, but not both
                    for gbitem in [self.dms.data_items.get(grpbase) for grpbase in self.groupby]:
                        if gbitem is not None:
                            gbitem_datatype = gbitem.get('columnType', None)
                            if gbitem_datatype is not None and gbitem_datatype == DATA_ITEM_DATATYPE_TIMESTAMP:
                                timestamp_dimension_used = gbitem[DATA_ITEM_NAME_KEY]
                                # it is assumed there can only be one timestamp-typed dimension used
                                break
                    if timestamp_dimension_used is None and 'shift_day' in self.groupby:
                        timestamp_dimension_used = 'shift_day'

                if self.frequency is not None:
                    # time frequency used, inspect the time range of the input dataframe, and use it to filter the cache
                    df_tmp = df.reset_index()
                    datetime_min = df_tmp[self.timestamp].min()
                    datetime_max = df_tmp[self.timestamp].max()
                    starting_point = util.period_start(datetime_min, freq=self.frequency)
                    ending_point = util.period_end(datetime_max, freq=self.frequency)  # not really used

                    self.logger.debug(
                        'aggregation_frequency=%s, aggregation_input_timerange=(%s, %s), aggregation_input_windowed_timerange=(%s, %s)' % (
                            str(self.frequency), str(datetime_min), str(datetime_max), str(starting_point),
                            str(ending_point)))

                    if not pd.isna(starting_point):
                        cache_df_index_names = list(df_loaded_from_cache.index.names)
                        current_df_index_names = list(df.index.names)
                        if self.is_df_index_columns_match(current_df_index_names, cache_df_index_names):
                            df_loaded_from_cache.reset_index(inplace=True)
                            df_loaded_from_cache = df_loaded_from_cache[
                                (df_loaded_from_cache[self.timestamp] >= starting_point.to_timestamp())]
                            df_loaded_from_cache.set_index(keys=cache_df_index_names, inplace=True)
                            self.logger.debug(
                                'aggregation_reload_df_refreshed_shape=%s' % (str(df_loaded_from_cache.shape)))
                            log_data_frame('aggregation_reload_df_refreshed', df_loaded_from_cache.head())
                elif timestamp_dimension_used:
                    # assumption: time goes by and old data eventually 'evict', for example, say for a daily dimension,
                    # as long as a day has passed by (not appearing in current batch), it never comes again
                    df_tmp = df.reset_index()
                    starting_point = df_tmp[timestamp_dimension_used].min()
                    ending_point = df_tmp[timestamp_dimension_used].max()  # not really used

                    self.logger.debug(
                        'aggregation_timestamp_dimension=%s, aggregation_input_dimensioned_timerange=(%s, %s)' % (
                            timestamp_dimension_used, str(starting_point), str(ending_point)))

                    if not pd.isna(starting_point):
                        cache_df_index_names = list(df_loaded_from_cache.index.names)
                        current_df_index_names = list(df.index.names)
                        if self.is_df_index_columns_match(current_df_index_names, cache_df_index_names):
                            df_loaded_from_cache.reset_index(inplace=True)
                            df_loaded_from_cache = df_loaded_from_cache[
                                (df_loaded_from_cache[timestamp_dimension_used] >= starting_point)]
                            df_loaded_from_cache.set_index(keys=cache_df_index_names, inplace=True)

                            self.logger.debug(
                                'aggregation_reload_df_refreshed_shape=%s, aggregation_reload_df_refreshed_index_dtypes=%s, aggregation_reload_df_refreshed_dtypes=%s' % (
                                    str(df_loaded_from_cache.shape),
                                    df_loaded_from_cache.index.to_frame().dtypes.to_dict(),
                                    df_loaded_from_cache.dtypes.to_dict()))
                            log_data_frame('aggregation_reload_df_refreshed', df_loaded_from_cache.head())
                else:
                    # TODO no timestamp, no 'eviction' possible in this case as all data must be kept, problem?
                    self.logger.warning(
                        'incremental update by reloading does not support non-time-based aggregation yet')

                if self.concat_only:
                    df = pd.concat([df_loaded_from_cache, df], sort=False)
                else:
                    column_labels = list(df.columns)
                    self.logger.debug('column_labels=%s' % column_labels)
                    columns_to_drop = list()
                    df_tmp = pd.merge(df, df_loaded_from_cache, how='outer', left_index=True, right_index=True,
                                      sort=False, suffixes=['', UNIQUE_EXTENSION_LABEL])
                    for col in column_labels:
                        # self.logger.debug('col=%s' % col)
                        if (col + UNIQUE_EXTENSION_LABEL) in df_tmp.columns:
                            # self.logger.debug('hit corresponding col=%s' % (col + UNIQUE_EXTENSION_LABEL))
                            df_tmp[col] = np.where(pd.notna(df_tmp[col]), df_tmp[col],
                                                   df_tmp[col + UNIQUE_EXTENSION_LABEL])
                            columns_to_drop.append(col + UNIQUE_EXTENSION_LABEL)
                    self.logger.debug('columns_to_drop=%s' % str(columns_to_drop))
                    df = df_tmp.drop(labels=columns_to_drop, axis=1)
            else:
                # no cache, do nothing
                pass

            self.logger.info('Cached data have been loaded from cache file into dataframe.')
            self.logger.debug('aggregation_reload_final_df_shape=%s, aggregation_reload_final_df_index_dtypes=%s,'
                              ' aggregation_reload_final_df_dtypes=%s' % (
                                  str(df.shape), df.index.to_frame().dtypes.to_dict(), df.dtypes.to_dict()))
            log_data_frame('aggregation_reload_final_df', df.head())

            # pyarrow does not handle mixed type column, here we force convert any column of type 'object' to str
            df = df.astype({col: str for col, dt in df.dtypes.to_dict().items() if str(dt) == 'object'})

            if self.production_mode:
                # persist the latest dataframe to repository
                self.df_cache.store_cache(dep_grain, grain, df)

                # Finish migration step: remove cache file with old name
                if remove_old_cache:
                    self.df_cache.delete_cache(dep_grain, grain, old_name=True)

        else:
            self.logger.info('No cache file handling because backtrack is active. '
                             'No cached data are loaded from cache file into dataframe.')

        return df

    def is_df_index_columns_match(self, current_df_index_names, cache_df_index_names):
        current_df_index_names_copy = current_df_index_names.copy()
        cache_df_index_names_copy = cache_df_index_names.copy()

        if set(current_df_index_names_copy) == set(cache_df_index_names_copy):
            return True
        else:
            error_message = ('Current dataframe index names { %s } is not matching with cached dataframe index { %s }. '
                             'Entity type name = %s, Entity type id = %s . Contact support to clean the data cache.') % (
                                ' , '.join(map(str, current_df_index_names)),
                                ' , '.join(map(str, cache_df_index_names)), self.dms.entity_type,
                                self.dms.entity_type_id)
            self.logger.error(error_message)
            raise Exception(error_message)

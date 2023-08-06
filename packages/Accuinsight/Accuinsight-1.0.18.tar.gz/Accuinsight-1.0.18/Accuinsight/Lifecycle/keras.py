import inspect
import json
import warnings
import os
import re
from collections import OrderedDict
import gorilla
import sys
import logging
import boto3
from pathlib import Path
import numpy as np
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import keras
from keras.callbacks import CSVLogger
from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.core.LcConst.LcConst import RUN_NAME_KERAS
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_visual_info_regressor
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, set_model_json_path, set_visual_csv_path, set_visual_json_path, set_best_model_h5_path, set_best_model_json_path, print_run_info, set_git_meta, set_python_dependencies, set_run_name, set_model_file_path, set_prefix_path
from Accuinsight.modeler.utils.dl_utils import delete_files_except_best, get_best_model_path
from Accuinsight.modeler.utils.runs_utils import get_aws_info, ProgressPercentage
from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
#from Accuinsight.modeler.core.notifier import notifierActor
from Accuinsight.modeler.utils.os_getenv import is_in_ipython, get_current_notebook
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi

logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

warnings.filterwarnings("ignore")

class accuinsight(object):
    def __init__(self):
        self.BucketInfo = None
        self.endpoint = None
        self.thresholds = None
        self.token = None
        self.channel_id = None
        self.message = None

    def get_file(self, sub_path):
        self.BucketInfo = get_aws_info(sub_path)
        BUCKET_TYPE = self.BucketInfo['bucket_type']
        BUCKET_NAME = self.BucketInfo['bucket_name']
        FILE_PATH = self.BucketInfo['file_path']
        FILE_NAME = self.BucketInfo['file_name']
        FILE_TYPE = self.BucketInfo['file_type']
        FILE_DELIM = self.BucketInfo['file_delim']
        ACCESS_KEY = self.BucketInfo['my_access_key']
        SECRET_KEY = self.BucketInfo['my_secret_key']
        REGION = self.BucketInfo['region']
        URL = self.BucketInfo['endpoint']

        ## path for saving data
        save_dir = os.path.join(Path.home(), 'data_from_catalog')
        if os.path.exists(save_dir) == False:
            os.mkdir(save_dir)
        else:
            pass
        
        save_path = os.path.join(str(Path.home()), save_dir, FILE_NAME)
        
        # endpoint (수정)
        #pre_url = 'https://' + BUCKET_NAME + '.' + URL
        #self.endpoint = os.path.join(pre_url, FILE_PATH)

        ### data catalog 사용시
        # https://accuinsight-dev.cloudz.co.kr/datacatalog/#/management/table/detail/24/156
        # '/databases/24/tables/156'

        regex = re.compile('(\d+)/tables/(\d+)')
        host = 'https://accuinsight-dev.cloudz.co.kr/datacatalog/#/management/table/detail'
        self.endpoint = os.path.join(host, regex.search(sub_path).group(1), regex.search(sub_path).group(2))
        
        client = boto3.client(BUCKET_TYPE,
                              aws_access_key_id = ACCESS_KEY,
                              aws_secret_access_key = SECRET_KEY,
                              region_name = REGION)

        transfer = boto3.s3.transfer.S3Transfer(client)
               
        progress = ProgressPercentage(client, BUCKET_NAME, FILE_PATH)

        sys.stdout.write('%s %s %s' % ('Downloading file...', FILE_NAME,  '\n'))
        transfer.download_file(BUCKET_NAME, FILE_PATH, save_path, callback=progress)
        logging.info(save_path)
        
    def set_slack(self, token = None, channel_id = None):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, message = None, thresholds = None):
        if message is not None and thresholds is not None:
            raise ValueError("'message'와 'thresholds' 두 개의 arguments를 동시에 입력할 수 없습니다.")
        else:
            self.message = message
            self.thresholds = thresholds

    def autolog(self, tag = None, best_weights = False):
        global description, endpoint, var_model_file_path, message, thresholds, token, channel_id
        description = tag
        endpoint = self.endpoint
        message = self.message
        thresholds = self.thresholds
        token = self.token
        channel_id = self.channel_id
        if best_weights == True:
            best_weights_on = True
        else:
            best_weights_on = False

        
        is_notebook = is_in_ipython()
        if is_notebook == True:
            var_model_file_path = get_current_notebook()
            _caller_globals = inspect.stack()[1][0].f_globals
            (
                mainfile,
                sources,
                dependencies
            ) = gather_sources_and_dependencies(
                globs=_caller_globals,
                save_git_info=False
            )
        else:
            _caller_globals = inspect.stack()[1][0].f_globals
            (
                mainfile,
                sources,
                dependencies
            ) = gather_sources_and_dependencies(
                globs=_caller_globals,
                save_git_info=True
            )
            var_model_file_path = mainfile['filename']

    
        class TrainHistoryCallbacks(keras.callbacks.Callback):
            def __init__(self, verbose = 1, mode = 'auto', period = 1):
                super(TrainHistoryCallbacks, self).__init__()
                self.verbose = verbose
                self.period = period
                self.best_epochs = 0
                self.epochs_since_last_save = 0
                self.mode = mode
        
            def on_train_begin(self, logs={}):
                if best_weights_on:
                    logging.info('Using autolog(best_weights=True)')
                else:
                    logging.info('Using autolog(best_weights=False)')
            
                global start
                start = get_time.now()
                self.run_id = func.get_run_id()
                self.model_type = get.model_type(self.model)
                self.model_summary = OrderedDict()
                self.model_summary['data_version'] = endpoint
                self.model_summary['model_description'] = description
                self.model_summary['logging_time'] = get_time.logging_time()
                self.model_summary['run_id'] = func.get_run_id()
                self.model_summary['model_type'] = get.model_type(self.model)
                
                if hasattr(self.model.loss, 'get_config'):
                    self.model_summary['loss_function'] = self.model.loss.get_config()['name']
                else:
                    self.model_summary['loss_function'] = self.model.loss
                
                self.model_summary['optimizer_info'] = {type(self.model.optimizer).__name__: self.model.optimizer.get_config()}
            
            
                '''[get best model] on_train_begin '''
                self.best_weights = self.model.get_weights()
              
                self.dict_path = path.get_file_path(self.model, usedFramework='keras')
            
                set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])
            
                set_run_name(self.model_type, self.run_id)
                set_python_dependencies(py_depenpency=dependencies)
            
            '''[get best model] on_epoch_end '''
            def on_epoch_end(self, epoch, logs=None):
                logs = logs or {}
                
                if epoch == 0:
                    if len(self.model.metrics_names) == 1 and 'loss' in self.model.metrics_names:
                        self.monitor = 'val_loss'
                    elif len(self.model.metrics_names) >= 2:
                        self.monitor = 'val_' + self.model.metrics_names[1]
                    # set monitoring option
                    if self.mode not in ['auto', 'min', 'max']:
                        warnings.warn('GetBest mode %s is unknown, '
                                      'fallback to auto mode.' % (self.mode), RuntimeWarning)
                        self.mode = 'auto'
                    if self.mode == 'min':
                        self.monitor_op = np.less
                        self.best = np.Inf
                    elif self.mode == 'max':
                        self.monitor_op = np.greater
                        self.best = -np.Inf
                    else:
                        if 'acc' in self.monitor or 'f1' in self.monitor:
                            self.monitor_op = np.greater
                            self.best = -np.Inf
                        else:
                            self.monitor_op = np.less
                            self.best = np.Inf
                else:
                    pass
                
                # Using best_weights
                if best_weights_on:
                    
                    # update best_weights
                    self.epochs_since_last_save += 1
                    if self.epochs_since_last_save >= 1:
                        self.epochs_since_last_save = 0
                        current = logs.get(self.monitor)
                        if current is None:
                            warnings.warn('Can pick best model only with %s available, '
                                      'skipping.' % (self.monitor), RuntimeWarning)
                        else:
                            if self.monitor_op(current, self.best):
#                                 if self.verbose > 0:
#                                     print('\n\nEpoch %05d: %s improved from %0.5f to %0.5f,'
#                                           ' storing weights.\n'
#                                           % (epoch + 1, self.monitor, self.best, current))
                                self.best = current
                                self.best_epochs = epoch + 1
                                self.best_weights = self.model.get_weights()
                            else:
                                pass
#                                 if self.verbose > 0:
#                                     print('\n\nEpoch %05d: %s did not improve\n' % (epoch + 1, self.monitor))

                    self.current_value = current
                    
                    # model save path
                    common_path = self.dict_path['save_model_path'] + self.model_summary['model_type'] + '-' + \
                    self.model_summary['run_id'] + '-epoch-' + str(epoch + 1).zfill(5) + '-' + self.monitor + '-' + str(current).zfill(5)
                    save_model_path = common_path + '.json'
                    save_weights_path = common_path + '.h5'

                    # model to JSON
                    model_json = self.model.to_json()
                    with open(save_model_path, "w") as json_file:
                        json_file.write(model_json)
                    # weights to H5
                    self.model.save_weights(save_weights_path)
    
                # Not using best_weights
                else:
                    self.last_epochs = epoch + 1
                    self.last_epoch_metric = logs.get(self.monitor)
                    
                    # model save path
                    common_path = self.dict_path['save_model_path'] + self.model_summary['model_type'] + '-' + \
                    self.model_summary['run_id'] + '-epoch-' + str(epoch + 1).zfill(5) + '-' + self.monitor + '-' + str(self.last_epoch_metric).zfill(5)
                    save_model_path = common_path + '.json'
                    save_weights_path = common_path + '.h5'

                    # model to JSON
                    model_json = self.model.to_json()
                    with open(save_model_path, "w") as json_file:
                        json_file.write(model_json)
                    # weights to H5
                    self.model.save_weights(save_weights_path)
                    
                    self.current_value = self.last_epoch_metric
            
            def on_train_end(self, logs={}):
                '''[get best model] on_train_end '''
                if self.verbose > 0:
                    print('Using epoch %05d with %s: %0.5f' % (self.best_epochs, self.monitor, self.best))
                self.model.set_weights(self.best_weights)  # set best model's weights
                
#                self.model_summary = OrderedDict()
#                self.model_summary['data_version'] = endpoint
#                self.model_summary['model_description'] = description
#                self.model_summary['logging_time'] = get_time.logging_time()
#                self.model_summary['run_id'] = self.run_id
#                self.model_summary['model_type'] = self.model_type
#
#                if hasattr(self.model.loss, 'get_config'):
#                    self.model_summary['loss_function'] = self.model.loss.get_config()['name']
#                else:
#                    self.model_summary['loss_function'] = self.model.loss
#
#                self.model_summary['optimizer_info'] = {type(self.model.optimizer).__name__: self.model.optimizer.get_config()}
                
                end = get_time.now()
                self.model_summary['time_delta'] = str(end - start)
                self.model_summary['selected_metrics'] = {self.monitor: self.best}
            
                # path for model_info.json
                self.path_for_setting_model_json = self.dict_path['model_json']
                set_model_json_path(self.path_for_setting_model_json)
            
                model_json_full_path = self.dict_path['model_json_full']
            
                with open(model_json_full_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.model_summary, save_file, indent="\t")
            
                if best_weights_on:
                    delete_files_except_best(run_id=self.model_summary['run_id'], epochs=str(self.best_epochs),
                                            path=self.dict_path)
                else:
                    delete_files_except_best(run_id=self.model_summary['run_id'], epochs=str(self.last_epochs),
                    path=self.dict_path)

                path_for_setting_model_json = self.dict_path['save_model_dir'] + get_best_model_path(run_id = self.run_id, path = self.dict_path)['json']
                set_best_model_json_path(path_for_setting_model_json)
                path_for_setting_model_h5 = self.dict_path['save_model_dir'] + get_best_model_path(run_id = self.run_id, path = self.dict_path)['h5']
                set_best_model_h5_path(path_for_setting_model_h5)
            
            
                start_ts = int(start.timestamp())
                end_ts = int(end.timestamp())
                delta_ts = end_ts - start_ts
            
                clear_runs(start_ts, end_ts, delta_ts)
                accuinsight._send_message(metric = self.monitor,
                                          current_value = self.current_value,
                                          message = self.message,
                                          thresholds = self.thresholds,
                                          token = self.token,
                                          channel_id = self.channel_id)
                modeler_rest = LifecycleRestApi(LcConst.BACK_END_API_URL,
                                                LcConst.BACK_END_API_PORT,
                                                LcConst.BACK_END_API_URI)
                modeler_rest.lc_create_run()
                accuinsight.off_autolog()
            
        
        class visualCallbacks(keras.callbacks.Callback):
            def __init__(self, x_validation=None, y_validation=None):
                self.x_val = x_validation
                self.y_val = y_validation

            def on_train_end(self, logs={}):

                self.dict_path = path.get_file_path(self.model, usedFramework='keras')

                # path for visual.json
                path_for_setting_visual_json = self.dict_path['visual_json']
                visual_json_full_path = self.dict_path['visual_json_full']
                set_visual_json_path(path_for_setting_visual_json)

                # classification
                if get.is_classification(self.model):
                    visual_classification_json = roc_pr_curve(self.model, self.x_val, self.y_val)

                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_classification_json, save_file, indent="\t")

                # regression
                else:
                    visual_regression_json = OrderedDict()
                    visual_regression_json['True_y'] = self.y_val.tolist()
                    visual_regression_json['Predicted_y'] = get_visual_info_regressor(self.model, self.x_val)

                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_regression_json, save_file, indent="\t")
            
        def run_and_log_function(self, original, args, kwargs, unlogged_params):

            dict_path = path.get_file_path(self, usedFramework='keras')
        
            path_for_setting_visual_csv = dict_path['visual_csv']
            visual_csv_full_path = dict_path['visual_csv_full']
        
            # set current run
            set_current_runs(RUN_NAME_KERAS)
            set_model_file_path(var_model_file_path)

            set_visual_csv_path(path_for_setting_visual_csv)

            csv_logger = CSVLogger(visual_csv_full_path, append=True, separator=';')
 
 
            ''' save json for visualization '''
            kwargs_dict = OrderedDict()
            
            for key, value in kwargs.items():
                kwargs_dict[key] = value
            
            # using validation_data argument
            if 'validation_data' in kwargs_dict.keys():
                validation_set = kwargs['validation_data']

                try:
                    x_val = validation_set[0]
                    y_val = validation_set[1]

                except:
                    iterator = iter(validation_set)
                    valid_set = next(iterator)
                    x_val = valid_set[0].numpy()
                    y_val = valid_set[1].numpy()
            
#            elif 'validation_split' in kwargs_dict.keys():
#                (x, y), validation_set = (data_adapter.train_validation_split((x,y), validation_split=kwargs_dict['validation_split']))
#                if validation_set:
#                    x_val, y_val, val_sample_weight = (data_adapter.unpack_x_y_sample_weight(validation_set))
#
            else:
                raise ValueError('"validation_data" or "validation_split" does not exist.')
            
            get_visual = visualCallbacks(x_validation=x_val, y_validation=y_val)


            if 'callbacks' in kwargs:
                kwargs['callbacks'] += [csv_logger]
                kwargs['callbacks'] += [get_visual]
                kwargs['callbacks'] += [TrainHistoryCallbacks()]
            
            else:
                kwargs['callbacks'] = [csv_logger]
                kwargs['callbacks'] += [get_visual]
                kwargs['callbacks'] += [TrainHistoryCallbacks()]

            fit_model = original(self, *args, **kwargs)
            return(fit_model)

        @gorilla.patch(keras.Model)
        def fit(self, *args, **kwargs):
            original = gorilla.get_original_attribute(keras.Model, 'fit')
            unlogged_params = ['self', 'x', 'y', 'callbacks', 'validation_data', 'verbose']
            return run_and_log_function(self, original, args, kwargs, unlogged_params)

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(keras.Model, 'fit', fit, settings=settings))


    def _send_message(metric=None, current_value=None, message=None, thresholds=None, token=None, channel_id=None):
        
        logger = logging.getLogger(__name__)
        
        if token is not None and channel_id is not None:
        
            if thresholds is not None:
                try:
                    if current_value >= thresholds:
                        msg = '[모델 학습 완료] ' + metric + '이 설정하신 thresolds: ' + str(thresholds) + '를 초과하였습니다.'
                        response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
                except SlackApiError as e:
                    logger.error(f"Error message: {e}")
                    
            elif message is not None:
                try:
                    msg = message
                    response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
                except SlackApiError as e:
                    logger.error(f"Error message: {e}")
        else:
            pass


#    def _send_message(metric = None, current_value = None, message = None, thresholds=None, token = None, channel_id = None):
#        if token is not None and channel_id is not None:
#            if thresholds is not None:
#                try:
#                    if current_value >= thresholds:
#                        msg = '[모델 학습 완료] ' + metric +'이 설정하신 thresolds: ' + str(thresholds) + '를 초과하였습니다.'
#                        response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
#                except SlackApiError as e:
#                    assert e.response["error"]
#            elif message is not None:
#                try:
#                    msg = message
#                    response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
#                except SlackApiError as e:
#                    assert e.response["error"]
#            else:
#                pass

    def off_autolog():
        def stop_log(self, original, args, kwargs, unlogged_params):
            fit_model = original(self, *args, **kwargs)
            return(fit_model)
        
        @gorilla.patch(keras.Model)
        def fit(self, *args, **kwargs):
            original = gorilla.get_original_attribute(keras.Model, 'fit')
            unlogged_params = ['self', 'x', 'y', 'callbacks', 'validation_data', 'verbose']
            return stop_log(self, original, args, kwargs, unlogged_params)

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(keras.Model, 'fit', fit, settings=settings))

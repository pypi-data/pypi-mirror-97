import os
import inspect
import json
import datetime
from collections import OrderedDict
import warnings
import sys
import logging
import boto3
from boto3.session import Session
import asyncio
from slack import WebClient
from slack.errors import SlackApiError
from pathlib import Path
from joblib import dump
from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_visual_info_regressor, get_true_y, get_visual_info_regressor
from Accuinsight.modeler.utils.runs_utils import get_aws_info, ProgressPercentage
from Accuinsight.modeler.core.sklearnModelType import REGRESSION, CLASSIFICATION
from Accuinsight.modeler.core.LcConst.LcConst import ALL_MODEL_PARAMS, SELECTED_PARAMS, SELECTED_METRICS, VALUE_ERROR, \
    LOGGING_TIME, LOGGING_RUN_ID, FITTED_MODEL, RUN_PREFIX_PATH, RUN_MODEL_JSON_PATH, RUN_MODEL_VISUAL_JSON_PATH, \
    RUN_MODEL_HOME_PATH, ENV_JUPYTER_HOME_DIR
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, print_run_info, \
    set_git_meta, set_python_dependencies, set_run_name, set_model_json_path, set_visual_json_path, set_model_file_path, set_prefix_path, set_best_model_joblib_path, _set_result_path, set_shap_json_path 
from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.utils.os_getenv import is_in_ipython, get_current_notebook
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi
from Accuinsight.modeler.core.feature_contribution import shap_value 


logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

warnings.filterwarnings("ignore")


class accuinsight(object):
    def __init__(self):
        self.StorageInfo = None
        self.endpoint = None

    def get_file(self, storage_json_file_name):
        global save_path, target_name, bucket_info
        
        # meta file 저장하는 폴더 만들면, 이 경로는 수정돼야 함.
        storage_info_json_path = os.path.join(ENV_JUPYTER_HOME_DIR, storage_json_file_name)
    
        with open(storage_info_json_path) as jsonFile:
            self.StorageInfo = json.load(jsonFile)
    
        ## define the target name
        target_name = self.StorageInfo['target']
        
        
        if 'host' in self.StorageInfo.keys():    # HDFS
            
            ## path for saving data
            save_dir = os.path.join(ENV_JUPYTER_HOME_DIR, 'data_from_hdfs')
            if os.path.exists(save_dir) == False:
                os.mkdir(save_dir)
            else:
                pass
            
            split_list = list(filter(None, self.StorageInfo['filePath'].split('/')))
            
            HOST = self.StorageInfo['host']
            PORT = int(self.StorageInfo['port'])
            FILE_PATH = self.StorageInfo['filePath']
            FILE_DIR = '/'
            for i in split_list[:len(split_list)-1]:
                FILE_DIR = os.path.join(FILE_DIR, i)
            FILE_NAME = split_list[-1]
            
            self.save_file_name = FILE_NAME.split('.')[0] + '_' + str(datetime.datetime.now().date()).replace('-', '') + '.' + FILE_NAME.split('.')[1]
            self.save_path = os.path.join(save_dir, self.save_file_name)
            self.endpoint = os.path.join('hdfs://', HOST, self.StorageInfo['port']) + FILE_PATH
            
            hdfs = HDFileSystem(host = HOST, port = PORT)
            hdfs.ls(FILE_DIR)

            sys.stdout.write('%s %s %s' % ('Downloading file...', FILE_NAME, '\n'))
            time.sleep(1)
            hdfs.get(FILE_PATH, self.save_path)
            logging.info(self.save_path)
        
        
        else:     # AWS-S3
            BUCKET_TYPE = self.StorageInfo['bucketType']
            BUCKET_NAME = self.StorageInfo['bucketName']
            FILE_PATH = self.StorageInfo['filePath']
            FILE_NAME = self.StorageInfo['fileName']
            #FILE_TYPE = self.StorageInfo['fileType']
            #FILE_DELIM = self.StorageInfo['fileDelim']
            ACCESS_KEY = self.StorageInfo['myAccessKey']
            SECRET_KEY = self.StorageInfo['mySecretKey']
            REGION = self.StorageInfo['region']
            URL = self.StorageInfo['endpoint']

            ## path for saving data
            save_dir = os.path.join(ENV_JUPYTER_HOME_DIR, 'data_from_aws')
            if os.path.exists(save_dir) == False:
                os.mkdir(save_dir)
            else:
                pass
  
            self.save_file_name = FILE_NAME.split('.')[0] + '_' + str(datetime.datetime.now().date()).replace('-', '') + '.' + FILE_NAME.split('.')[1]
            save_path = os.path.join(save_dir, self.save_file_name)

            # endpoint
            pre_url = 'https://' + BUCKET_NAME + '.' + URL
            self.endpoint = os.path.join(pre_url, FILE_PATH)

            client = boto3.client(BUCKET_TYPE,
                                  aws_access_key_id=ACCESS_KEY,
                                  aws_secret_access_key=SECRET_KEY,
                                  region_name=REGION)

            transfer = boto3.s3.transfer.S3Transfer(client)

            progress = ProgressPercentage(client, BUCKET_NAME, FILE_PATH)
    
            sys.stdout.write('%s %s %s' % ('Downloading file...', FILE_NAME, '\n'))
            transfer.download_file(BUCKET_NAME, FILE_PATH, save_path, callback=progress)
            logging.info(save_path)
        
        bucket_info = self.StorageInfo
    
    def set_slack(self, token = None, channel_id = None):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, message = None):
        if message is not None:
            try:
                message = message
                response = WebClient(token=self.token).chat_postMessage(channel=self.channel_id, text=message)
            except SlackApiError as e:
                assert e.response["error"]
        else:
            raise ValueError('message를 입력해주세요.')


    class add_experiment(object):
        def __init__(self, model_name, *args, model_monitor=False):
            if model_monitor == True:
                self.shap_on = True
                logging.info('Using add_experiment(model_monitor=True)')
            else:
                self.shap_on = False
                logging.info('Using add_experiment(model_monitor=False)')
            
            self.model_name = model_name
        
            is_notebook = is_in_ipython()
            if is_notebook == True:
                self.var_model_file_path = get_current_notebook()
                _caller_globals = inspect.stack()[1][0].f_globals
                (
                    self.mainfile,
                    self.sources,
                    self.dependencies
                ) = gather_sources_and_dependencies(
                    globs=_caller_globals,
                    save_git_info=False
                )
            else:
                _caller_globals = inspect.stack()[1][0].f_globals
                (
                    self.mainfile,
                    self.sources,
                    self.dependencies
                ) = gather_sources_and_dependencies(
                    globs=_caller_globals,
                    save_git_info=True
                )
                self.var_model_file_path = self.mainfile['filename']

            self.fitted_model = get.model_type(self.model_name)          # fitted model type
            self.json_path = OrderedDict()                               # path
            self.selected_params = []                                    # log params
            self.selected_metrics = OrderedDict()                        # log metrics
            self.summary_info = OrderedDict()                            # final results
            self.error_log = []                                          # error log
            self.vis_info = None                                         # visualization info - classifier
            self.dict_path = path.get_file_path(self.model_name)

            set_current_runs(get.model_type(self.model_name))
            _set_result_path(self.dict_path)

            # visualization function
            if len(args) == 2:
                self.xval = args[0]
                self.yval = args[1]

            elif len(args) == 4:
                self.xtrain = args[0]
                self.ytrain = args[1]
                self.xval = args[2]
                self.yval = args[3]
    
            else:
                raise ValueError('Check the arguments of function - add_experiment(model_name, X_val, y_val) or add_experiment(model_name, X_train, y_train, X_val, y_val)')

            # classifier
            if any(i in self.fitted_model for i in CLASSIFICATION):
                self.vis_info = roc_pr_curve(self.model_name, self.xval, self.yval)

            # regressor
            elif any(i in self.fitted_model for i in REGRESSION):
                self.ypred = get_visual_info_regressor(self.model_name, self.xval)
                
            # sklearn/xgboost/lightgbm
            get_from_model = get.from_model(self.model_name)
            self.all_model_params = get_from_model.all_params()
            self.model_param_keys = get_from_model.param_keys()

            set_model_file_path(self.var_model_file_path)

            if hasattr(self, 'mainfile'):
                set_git_meta(fileinfo=self.mainfile)
            if hasattr(self, 'dependencies'):
                set_python_dependencies(py_depenpency=self.dependencies)

        def __enter__(self):
            self.start_time = get_time.now()
            self.summary_info[LOGGING_TIME] = get_time.logging_time()
            self.summary_info[LOGGING_RUN_ID] = func.get_run_id()
            self.summary_info[FITTED_MODEL] = self.fitted_model

            set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])
            set_run_name(self.fitted_model, self.summary_info[LOGGING_RUN_ID])

            return(self)

        def __exit__(self, a, b, c):
            self.summary_info[ALL_MODEL_PARAMS] = self.all_model_params
            self.summary_info[SELECTED_PARAMS] = self.selected_params
            self.summary_info[SELECTED_METRICS] = self.selected_metrics
            self.summary_info[VALUE_ERROR] = self.error_log

            # model_monitor = True
            self.run_id = self.summary_info[LOGGING_RUN_ID]
            
            if self.shap_on == True:
                try:
                    self.feature_name = get.feature_name(save_path, bucket_info, target_name)
                except:
                    self.feature_name = None
                self.run_id = self.fitted_model + '-' + self.run_id
                
                self.shap_value = shap_value(self.model_name, self.xtrain, self.feature_name)
                
                # path for shap.json
                shap_json_full_path = self.dict_path['shap_json_full']
                set_shap_json_path(self.dict_path['shap_json'])
                
                with open(shap_json_full_path, 'w', encoding = 'utf-8') as save_file:
                    json.dump(self.shap_value, save_file, indent='\t')
                
            else:   
                pass
                
            # visualization
            if any(i in self.fitted_model for i in CLASSIFICATION):

                # path for visual.json
                visual_json_full_path = self.dict_path['visual_json_full']
                set_visual_json_path(self.dict_path['visual_json'])

                with open(visual_json_full_path, 'w', encoding='utf-8') as save_file1:
                    json.dump(self.vis_info, save_file1, indent="\t")

            elif any(i in self.fitted_model for i in REGRESSION):
                temp_yval = get_true_y(self.yval)
                if len(temp_yval) <= 5000:
                    self.summary_info['True_y'] = temp_yval
                    self.summary_info['Predicted_y'] = get_visual_info_regressor(self.model_name, self.xval)
                else:
                    self.summary_info['True_y'] = None
                    self.summary_info['Predicted_y'] = None

            self.summary_info['ValueError'] = self.error_log

            if not self.summary_info['ValueError']:
                # path for model_info.json
                model_json_full_path = self.dict_path['model_json_full']
                set_model_json_path(self.dict_path['model_json'])

                with open(model_json_full_path, 'w', encoding='utf-8') as save_file2:
                    json.dump(self.summary_info, save_file2, indent="\t")
            else:
                pass

            # model save
            save_model_path = self.dict_path['save_model_joblib'] + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'
            path_for_setting_model_joblib = self.dict_path['save_model_dir'] + '/' + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'

            set_best_model_joblib_path(path_for_setting_model_joblib)

            dump(self.model_name, save_model_path)

            start_time = int(self.start_time.timestamp()*1000)
            end_time = int(get_time.now().timestamp()*1000)
            delta_ts = end_time - start_time

            clear_runs(start_time, end_time, delta_ts)
            modeler_rest = LifecycleRestApi(LcConst.BACK_END_API_URL,
                                            LcConst.BACK_END_API_PORT,
                                            LcConst.BACK_END_API_URI)
            modeler_rest.lc_create_run()


        def log_params(self, param = None):
            # sklearn/xgboost/lightgbm
            if param:
                
                if param in self.model_param_keys:
                    return(self.selected_params.append(param))

                else:
                    self.error_log.append(True)
                    raise ValueError('"' + param + '"' + ' does not exist in the model.')

        def log_metrics(self, metric_name, defined_metric):
            self.selected_metrics[metric_name] = defined_metric

        def log_tag(self, description):
            self.summary_info['tag'] = description

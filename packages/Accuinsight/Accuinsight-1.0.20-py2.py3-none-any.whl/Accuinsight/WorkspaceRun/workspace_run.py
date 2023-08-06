import argparse
import subprocess
from Accuinsight.modeler.clients.modeler_api import WorkspaceRunRestApi
from Accuinsight.modeler.entities.workspace_run_log import WorkspaceRunLog
from Accuinsight.modeler.core.LcConst import LcConst


class WorkspaceRun:
    """
        Object for running code and sending the result to backend.
    """
    def __init__(self):
        self.workspace_run_log = WorkspaceRunLog()
        self.workspace_run_api = WorkspaceRunRestApi(LcConst.BACK_END_API_URL,
                                                     LcConst.BACK_END_API_PORT,
                                                     LcConst.BACK_END_API_URI)
        self.code_path = None

    def exec_code(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--workspaceRunId', default=None)
        parser.add_argument('--codePath', default=None)
        parser.add_argument('--stopFlag', default=False)
        parser.add_argument('--stopTimeout', default=60)

        args, unknown = parser.parse_known_args()
        args_dict = vars(args)

        self.code_path = args_dict['codePath']
        self.workspace_run_log.workspace_run_id = args_dict['workspaceRunId']
        self.workspace_run_log.stop_flag = args_dict['stopFlag']
        self.workspace_run_log.stop_timeout = args_dict['stopTimeout']

        if not self.code_path:
            raise Exception("codePath cannot be none")

        try:
            subprocess.run("python3 -u %s > "
                           "/tmp/output_%s.log 2>&1"
                           % (self.code_path, self.workspace_run_log.workspace_run_id), shell=True, encoding='UTF-8')\
                .check_returncode()
            self.workspace_run_log.is_success = True
        except subprocess.CalledProcessError:
            self.workspace_run_log.is_success = False
        finally:
            self.workspace_run_api.call_rest_api(self.workspace_run_log.get_result_param())


if __name__ == "__main__":
    workspace_run = WorkspaceRun()
    workspace_run.exec_code()

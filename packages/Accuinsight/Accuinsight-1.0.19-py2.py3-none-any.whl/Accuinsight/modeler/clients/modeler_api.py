"""
This http client send run's results data to modeler back-end server
"""

from Accuinsight.modeler.store.tracking.life_cycle_store import RestStore as LcRestStore
from Accuinsight.modeler.store.tracking.monitoring_deploy_store import RestStore as MonitoringDeployRestStore
from Accuinsight.modeler.store.tracking.workspace_run_store import RestStore as WorkspaceRunRestStore
from Accuinsight.modeler.utils.rest_utils import ModelerHostCreds
from Accuinsight.modeler.core.LcConst import LcConst

_DEFAULT_USER_ID = "unknown"


class LifecycleRestApi:
    def __init__(self, host_url, port, uri):
        self.base_url = 'http://' + host_url + ':' + str(port) + '/' + uri

    def lc_create_run(self):
        """Create run."""

        store = LcRestStore(lambda: ModelerHostCreds(self.base_url))
        run = store.lc_create_run()
        return run


class DeployLogRestApi:
    def __init__(self, host_url, port, uri):
        self.base_url = 'http://' + host_url + ':' + str(port) + '/' + uri

    def call_rest_api(self, method, param, mode="logging"):
        store = MonitoringDeployRestStore(ModelerHostCreds(self.base_url))
        response = store.call_endpoint(method, param, mode)

        return response


class WorkspaceRunRestApi:
    def __init__(self, host_url, port, uri):
        self.base_url = 'http://' + host_url + ':' + str(port) + '/' + uri

    def call_rest_api(self, param):
        store = WorkspaceRunRestStore(ModelerHostCreds(self.base_url))
        response = store.call_endpoint(param)

        return response


if __name__ == "__main__":
    modeler_rest = LifecycleRestApi(LcConst.BACK_END_API_URL,
                                    LcConst.BACK_END_API_PORT,
                                    LcConst.BACK_END_API_URI)

    modeler_rest.lc_create_run()

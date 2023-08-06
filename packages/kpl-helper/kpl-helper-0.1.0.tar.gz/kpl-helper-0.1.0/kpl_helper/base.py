import requests
from requests.adapters import HTTPAdapter
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("kpl-helper")

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))


class _BaseConfig:
    def __init__(self):
        _inner = os.getenv("KPL_INNER")
        self._inner = False if _inner is None else True
        if not self._inner:
            return
        # KPL_ENV: notebook/pipeline/deploy
        self._env_type = os.getenv("KPL_ENV")
        self._input_root = os.getenv("KPL_ENV_INPUT_ROOT_PATH")
        self._output_root = os.getenv("KPL_ENV_OUTPUT_ROOT_PATH", "/")
        self._parameter = os.getenv("KPL_ENV_PARAMETER")
        self._task_id = os.getenv("KPL_ENV_TASK_ID", 0)
        # TODO: remove  KPL_METRIC_TOKEN, KPL_METRIC_API
        self._metric_api = os.getenv("KPL_METRIC_API")
        self._metric_token = os.getenv("KPL_METRIC_TOKEN")
        self._api_url = os.getenv("KPL_ENV_INTERNAL_API_HOST", "")
        if not self._api_url.endswith("/"):
            self._api_url = self._api_url + "/"
        jwt_token_path = os.getenv("KPL_TOKEN_LOCATE")
        with open(jwt_token_path) as fi:
            self._jwt_token = fi.read().strip()

    def get_api_url(self):
        if not self._inner:
            return ""
        if self._api_url:
            return self._api_url
        return 'http://seetaas--monitor.seetaas.svc.cluster.local:8920/'

    def get_jwt_token(self):
        if not self._inner:
            return ""
        return self._jwt_token

    def get_inner(self):
        return self._inner

    def get_input_root(self):
        if not self._inner:
            return ""
        return self._input_root

    def get_output_root(self):
        if not self._inner:
            return ""
        return self._output_root

    def get_parameter(self):
        if not self._inner:
            return "{}"
        return self._parameter

    def get_metric_api(self):
        if not self._inner:
            return ""
        return self._metric_api

    def get_metric_token(self):
        if not self._inner:
            return ""
        return self._metric_token

    def get_env_type(self):
        if not self._inner:
            return None
        return self._env_type

    def get_cluster(self):
        pass


__base_config = None


def get_config():
    global __base_config
    if __base_config is None:
        __base_config = _BaseConfig()
    return __base_config


def ready():
    logging.info("[kpl-helper]: ready for using.")


def done():
    logging.info("[kpl-helper]: execute kpl done()")


class _MsgType:
    NewMetric = "NewMetric"
    MetricData = "MetricData"


class _ResultType:
    SCALAR_RESULT = 'scalar_result'  # 用于如Rank1，Rank5，LFW，MegaFace测试协议输出的单精度值测试结果
    CURVE_RESULT = 'curve_result'  # 用于如ROC测试协议输出的测试曲线
    PROGRESS = 'progress'


def _send_metric(body):
    if not get_config().get_inner():
        return
    if len(get_config().get_metric_api()) == 0 or len(get_config().get_metric_token()) == 0:
        raise Exception("You should run your algorithm inner SeeTaaS or AutoDL platform")
    try:
        if not isinstance(body, list):
            body = [body]
        resp = session.post('{}/uploadTaskMetrics'.format(get_config().get_metric_api()),
                            json={
                                "token": get_config().get_metric_token(),
                                "items": body
                            },
                            timeout=5)
        if resp.status_code != 200:
            logger.error("send metrics http code: {}. content: {}".format(resp.status_code, resp.content))
    except requests.RequestException as e:
        logger.error('Could not reach metric api. detail: {}'.format(e))


def _send_result(result_type, name, value):
    if not get_config().get_inner():
        return
    if len(get_config().get_metric_api()) == 0 or len(get_config().get_metric_token()) == 0:
        raise Exception("You should run your algorithm inner SeeTaaS or AutoDL platform")
    try:
        resp = session.post('{}/updateTaskAttribute'.format(get_config().get_metric_api()),
                            json={
                                "token": get_config().get_metric_token(),
                                "type": result_type,
                                "name": name,
                                "value": value
                            },
                            timeout=5)
        if resp.status_code != 200:
            logger.error("send evaluate result http code: {}. content: {}".format(resp.status_code, resp.content))
    except requests.RequestException as e:
        logger.error('Could not reach evaluate result api. detail: {}'.format(e))

from kpl_helper.base import _send_result, _ResultType, get_config
from kpl_helper.base import logger
import warnings


def send_scalar_result(**results):
    """
    发送单数值测试结果
    eg: send_scalar_result(top1=0.92, top2=0.98)
    """
    warnings.warn(
        "`send_scalar_result` is deprecated; use the `TensorBoard` instead")
    if not get_config().get_inner():
        return
    for k, v in results.items():
        _send_result(_ResultType.SCALAR_RESULT, k, v)


def send_curve_result(title, x_name, x_points, y_name, y_points):
    """
    发送测试协议输出为曲线的测试结果
    eg: send_curve_result("Recall and Precision", "recall", [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], "precision",[0.0, 0.8, 0.89, 0.94, 0.96, 1.0])
    """
    warnings.warn(
        "`send_curve_result` is deprecated; use the `TensorBoard` instead")
    if not get_config().get_inner():
        return
    if len(x_points) != len(y_points):
        logger.error("send curve result len(x_points)={} VS len(y_points)={}".format(len(x_points), len(y_points)))
        return
    data = []
    for x, y in zip(x_points, y_points):
        data.append([x, y])
    value = {
        "x": x_name,
        "y": y_name,
        "data": data
    }
    _send_result(_ResultType.CURVE_RESULT, title, value)



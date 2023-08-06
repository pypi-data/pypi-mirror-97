from kpl_helper.base import _ResultType, _send_result, logger, get_config


def send_progress(progress):
    """
    :param progress: program progress. value range：0.0 ~ 1.0 (i.e. 0.0% ~ 100%)
    :return:
    """
    if not get_config().get_inner():
        return
    if not (0.0 <= progress <= 1.0):
        logger.error("progress value error. should in range [0.0: 1.0]. but get {}".format(progress))
        if progress < 0.0: progress = 0.0
        if progress > 1.0: progress = 1.0
    _send_result(_ResultType.PROGRESS, "progress", progress)


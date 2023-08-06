from kpl_helper.base import get_config
import os
import logging
logger = logging.getLogger("kpl-helper")


def get_input_path(key, default=""):
    inner = get_config().get_inner()
    if not inner:
        return default
    root = get_config().get_input_root()
    path = os.path.join(root, str(key))
    if not os.path.exists(path):
        raise Exception("input direction not exists: {}".format(path))
    return path


def get_output_path(key, default=""):
    inner = get_config().get_inner()
    if not inner:
        return default
    root = get_config().get_output_root()
    path = os.path.join(root, str(key))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


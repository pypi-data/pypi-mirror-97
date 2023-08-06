# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from kpl_helper.base import get_config
import sys
import json
import os
import logging
import yaml

logger = logging.getLogger("kpl-helper")


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        super(DotDict, self).__init__()
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

    def __delitem__(self, key):
        super(DotDict, self).__delitem__(key)
        del self.__dict__[key]

    # setstate and getstate is for pickle
    def __getstate__(self):
        pass

    def __setstate__(self, *args, **kwargs):
        pass


def _load_json(str):
    if sys.version_info.major >= 3:
        return json.loads(str)

    def json_loads_byteified(json_text):
        return _byteify(
            json.loads(json_text, object_hook=_byteify),
            ignore_dicts=True
        )

    def _byteify(data, ignore_dicts=False):
        if isinstance(data, unicode):
            return data.encode('utf-8')
        if isinstance(data, list):
            return [_byteify(item, ignore_dicts=True) for item in data]
        if isinstance(data, dict) and not ignore_dicts:
            return {
                _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
            }
        return data

    return json_loads_byteified(str)


_parameter = None


def get_parameter(default=None):
    """
    :param default: path to parameter.yml
    :return: parameter object
    """
    global _parameter
    if _parameter is not None:
        return _parameter
    if get_config().get_inner() and get_config().get_env_type() != "notebook":
        parameter = get_config().get_parameter()
        _parameter = DotDict(_load_json(parameter)) if parameter else None
        return _parameter
    if default:
        with open(default) as fi:
            param = yaml.safe_load(fi)
            _parameter = DotDict(param)
            return _parameter
    raise Exception("Not found parameter")


def write_parameter():
    argv = sys.argv
    if argv[1] == 'write' and len(argv) > 2:
        output_yml = argv[2]
    else:
        logger.error('Write Failed !!!\nUsage `helper write <yml file>` to write parameters to yml')
        sys.exit(1)
    parameter = get_config().get_parameter()
    try:
        if parameter is None:
            raise ValueError('Parameter is None')
        path = os.path.dirname(output_yml)
        if path and not os.path.isdir(path):
            os.makedirs(path)
        with open(output_yml, 'w') as fo:
            fo.write(parameter)
    except Exception as e:
        logger.error('Could get parameters. {}'.format(e))

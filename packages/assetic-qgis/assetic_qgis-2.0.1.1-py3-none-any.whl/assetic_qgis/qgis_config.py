# coding: utf-8
"""
    assetic.config  (config.py)
    Configure assetic_qgis
"""
from assetic.tools.shared.config_base import ConfigBase


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class QgisConfig(ConfigBase):
    def __init__(self, messager=None, xmlconfigfile=None, inifile=None, logfile=None, loglevelname=None):
        super().__init__(messager, xmlconfigfile, inifile, logfile, loglevelname)

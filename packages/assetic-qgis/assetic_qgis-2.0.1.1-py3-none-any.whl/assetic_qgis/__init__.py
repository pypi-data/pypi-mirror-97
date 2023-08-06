# coding: utf-8

"""
    Assetic QGIS Integration API
"""

import logging
import os
import sys

from .__version__ import __version__
from .initialise import Initialise
from .qgis_config import QgisConfig
from .tools.qgis_layertools import QGISLayerTools

# setup logging with some hardcoded settings so we can trap any initialisation
# errors which can be more difficult to trap when running in QGIS
logger = logging.getLogger(__name__)
appdata = os.environ.get("APPDATA")
logfile = os.path.abspath(appdata + r"\Assetic\qgis.log")

f_handler = logging.FileHandler(logfile)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
f_handler.setFormatter(formatter)
logger.addHandler(f_handler)
logger.setLevel(logging.INFO)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value,
                                                 exc_traceback))


sys.excepthook = handle_uncaught_exception

# coding: utf-8
"""
    Initialise package
"""

from assetic.tools.shared import InitialiseBase

from assetic_qgis import __version__


class Initialise(InitialiseBase):
    def __init__(self, config):
        super().__init__(__version__, config=config)


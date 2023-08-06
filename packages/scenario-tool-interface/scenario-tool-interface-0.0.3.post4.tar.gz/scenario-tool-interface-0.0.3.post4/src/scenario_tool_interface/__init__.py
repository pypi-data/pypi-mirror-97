# -*- coding: utf-8 -*-
"""
This module provides access to the Scenario-Tool's REST API to create and run scenarios and manage models
"""
from pkg_resources import get_distribution, DistributionNotFound

from scenario_tool_interface.sti import ScenarioToolInterface, AccessLevel

from scenario_tool_interface.json2dynamind import Json2DynaMindXML
from scenario_tool_interface.dynamind2json import DynaMindXML2Json

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'scenario-tool-interface'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = '0.0.2'
finally:
    del get_distribution, DistributionNotFound

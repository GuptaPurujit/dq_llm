import os
import sys
import json
from configparser import SafeConfigParser
from functools import reduce
sys.path.insert(0, os.getcwd())

class ConfigUtility(object):
    """Class for Configuration Utility"""
    # Parametrized constructor with Configuration file as input
    def __init__(self, conf_file=None, conf=None):
        try:
            if conf_file is not None:
                config_fp = open(conf_file)
                self.json_configuration = json.load(config_fp)
            elif conf is not None:
                self.json_configuration = conf
            else:
                self.json_configuration = {}
        except BaseException:
            pass

    # #################################### Get Configuration ####################################
    #   Purpose : This method will read the value of a configuration parameter corresponding to a
    #             section in the configuration file
    #   Input   : Section in the configuration file, Configuration Name
    #   Output  : Returns the value of the configuration parameter present in the configuration file
    # ##############################################################################################
    def get_configuration(self, conf_hierarchy):
        """Method to get the configuration"""
        try:
            return reduce(
                lambda dictionary,
                key: dictionary[key],
                conf_hierarchy,
                self.json_configuration)
        except BaseException:
            pass
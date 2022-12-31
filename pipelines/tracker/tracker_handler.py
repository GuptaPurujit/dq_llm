"""
Handler For Weight Tracker Pipeline
"""

__author__ = 'Purujit'

import os
import sys
from datetime import datetime
import logger_file
from db_connection import DBConnection
import constants
from constants import Tables
from config_utility import ConfigUtility
from common_queries import *

MODULE_NAME = "weight_tracker_handler.py"
logger = logger_file.get_logger(module_name=MODULE_NAME)

class WeightTrackerHandler:
    def __init__(self):
        self.configuration = ConfigUtility(constants.ENVIRONMENT_PARAMS_FILE)
        self.mysql_host = self.configuration.get_configuration([constants.ENVIRONMENT_PARAMS_KEYS, "mysql_host"])
        self.mysql_port = self.configuration.get_configuration([constants.ENVIRONMENT_PARAMS_KEYS, "mysql_port"])
        self.mysql_user = self.configuration.get_configuration([constants.ENVIRONMENT_PARAMS_KEYS, "mysql_user"])
        self.mysql_password = self.configuration.get_configuration([constants.ENVIRONMENT_PARAMS_KEYS, \
            "mysql_password"])
        self.mysql_db = self.configuration.get_configuration([constants.ENVIRONMENT_PARAMS_KEYS, "mysql_db"])
        self.db_connection_obj = DBConnection(host=self.mysql_host, port=self.mysql_port, \
            user=self.mysql_user, password=self.mysql_password, db=self.mysql_db)

    def main(self, weight, user_id, pipeline_name):
        # fetch pipeline_user_id for the pipeline_name
        query = FETCH_PIPELINE_USER_ID_QUERY.format(user_id=user_id, pipeline_name=pipeline_name)
        logger.info("Query to fetch pipeline user id is: \n%s", query)
        pipline_user_id_res = self.db_connection_obj(query, get_single_result=True)
        if not pipline_user_id_res:
            raise Exception("Could not find pipeline user id")
        pipeline_user_id = pipline_user_id_res[0]['pipeline_user_id']

        # get the weight json
        query = FETCH_PIPELINE_JSON_QUERY.format(table_name=Tables.WEIGHT_TRACKER_DTL, \
            pipeline_user_Id=pipeline_user_id)
        logger.info("Query to fetch pipeline json is: \n%s", query)
        pipeline_json_res = self.db_connection_obj(query, get_single_result=True)
        if not pipeline_json_res:
            raise Exception("Could not find pipeline json")
        pipeline_json = pipeline_json_res[0]['pipeline_json']

        # append weigth with approp details 
        """
        example json
        {
            "datetime": "datetime.now()",
            "weigth": 78 kg
        }
        """ 
        day = datetime.now()
        new_weight_json = {
            "Day": day,
            "Weight": weight
        }
        pipeline_json = {**pipeline_json, **new_weight_json}

        # update RDS
        query = UPDATE_PIPELINE_JSON_QUERY.format(table_name=Tables.WEIGTH_TRACKER_DTL, \
            pipeline_user_id=pipeline_user_id, pipeline_json=pipeline_json)
        logger.info("Query to update pipeline json is: \n%s", query)
        self.db_connection_obj(query)

        # return json
        return pipeline_json
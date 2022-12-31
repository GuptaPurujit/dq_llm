"""
Handler For Weight Tracker Pipeline
"""

__author__ = 'Purujit'

import os
import sys
from datetime import datetime
import json
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
        self.db_connection_obj = DBConnection(host=self.mysql_host, port=str(self.mysql_port), \
            user=self.mysql_user, password=self.mysql_password, db=self.mysql_db)
    
    def main(self, weight, user_id, pipeline_name):
        # fetch pipeline_user_id for the pipeline_name
        query = FETCH_PIPELINE_USER_ID_QUERY.format(user_id=user_id, pipeline_name=pipeline_name)
        logger.info("Query to fetch pipeline user id is: \n%s", query)
        pipline_user_id_res = self.db_connection_obj.execute_query_mysql(query, get_single_result=True)
        if not pipline_user_id_res:
            raise Exception("Could not find pipeline user id")
        pipeline_user_id = pipline_user_id_res['pipeline_user_id']

        # get the weight json
        query = FETCH_PIPELINE_JSON_QUERY.format(table_name=Tables.WEIGHT_TRACKER_DTL, \
            pipeline_user_id=pipeline_user_id)
        logger.info("Query to fetch pipeline json is: \n%s", query)
        pipeline_json_res = self.db_connection_obj.execute_query_mysql(query, get_single_result=True)
        if not pipeline_json_res:
            raise Exception("Could not find pipeline json")
        pipeline_json = pipeline_json_res['pipeline_json']

        # append weight with approp details 
        day = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        new_weight_json = {
            "Day": day,
            "Weight": weight
        }
        new_weight_json = json.loads(json.dumps(new_weight_json))
        if pipeline_json:
            pipeline_json = json.loads(pipeline_json)
            pipeline_json = {**pipeline_json, **new_weight_json} 
        else:
            pipeline_json = [new_weight_json]

        logger.info("New pipeline json is : %s", pipeline_json)
        # update RDS
        query = UPDATE_PIPELINE_JSON_QUERY.format(table_name=Tables.WEIGHT_TRACKER_DTL, \
            pipeline_user_id=pipeline_user_id, pipeline_json=json.dumps(pipeline_json))
        logger.info("Query to update pipeline json is: \n%s", query)
        self.db_connection_obj.execute_query_mysql(query)

        # return json
        return pipeline_json

if __name__ == "__main__":
    pipeline_json = WeightTrackerHandler().main(70, 1, "weight_tracker")

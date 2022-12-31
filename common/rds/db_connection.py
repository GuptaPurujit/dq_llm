"""
Module for establishing connection to DB and execting Query
"""

__author__ = 'Purujit'

import os
import sys
import traceback
import mysql.connector
import logger_file 

MODULE_NAME = "db_connection.py"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
logger = logger_file.get_logger(module_name=MODULE_NAME)

class DBConnection:
    def __init__(self, host=None, port=3306, user=None, password=None, db=None):
        try:
            status_message = "Starting function to fetch my-sql connection"
            logger.info(status_message)
            # Preparing MySQL connection using the connection parameters
            # provided in environment
            if len(host) == 0 or len(user) == 0 or len(
                    password) == 0 or len(db) == 0 or len(port) == 0:
                status_message = "Please provide all the required inputs - host,username,password,db"
                logger.error(status_message)
                raise Exception
        
            self.mysql_connection = mysql.connector.connect(
                    host=host, user=user, passwd=password, database=db, port=int(port))
            status_message = "Connection to MySQL successful"
            logger.info(status_message)
        
        except Exception as exception:
            error = "ERROR in " + \
                    " ERROR MESSAGE: " + str(exception)
            logger.error(error)
            raise exception
    
    # This acts as the de-constructor for the objects of this class
    def __exit__(self, type, value, traceback):
        for file in self.files:
            os.unlink(file)
    
    #################################### Execute MySQL query##################
    # Purpose            :   Execute a query in MySQL
    # Input              :   Query String
    # Output             :   Tuple of tuples in case of a select query, None otherwise
    ##########################################################################

    def execute_query_mysql(self, query, get_single_result=None, tuple_data=None):
        """ Module for executing queries"""
        try:
            status_message = "Starting function to execute a MySQLquery : " + \
                str(query)
            logger.info(status_message)
            if query:
                query = query.strip()

            cursor = self.mysql_connection.cursor(dictionary=True)
            status_message = "Created connection to MySQL"
            logger.info(status_message)
            status_message = "Executing query on MySQL"
            logger.info(status_message)
            if query.lower().startswith("select"):
                cursor.execute(query)
                if get_single_result:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            elif query.lower().startswith("insert into"):
                result = cursor.execute(query)
                result = cursor.lastrowid
                cursor.execute("commit")
            else:
                if tuple_data is not None:
                    cursor.executemany(query, tuple_data)
                else:
                    cursor.execute(query)
                cursor.execute("commit")
                result = ""
            status_message = "Executed query on MySQL with result : " + \
                str(result)
            logger.info(status_message)
            return result
        except Exception as exception:
            error = "ERROR in module " + \
                    " ERROR MESSAGE: " + str(traceback.format_exc())
            logger.error(error)
            raise exception
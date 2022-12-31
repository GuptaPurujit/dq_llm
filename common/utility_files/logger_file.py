"""
Module for Logging
"""

__author__ = 'Purujit'

import sys
import logging
import os
from datetime import datetime

sys.path.insert(0, os.getcwd())

def get_logger(module_name):
    """
    Function to get logger object
    """
    # to get an object of root logger, if exists
    logger = logging.getLogger()

    if len(logger.handlers) > 0:
        for handler in logger.handlers:
            # remove root logger, if exists
            logger.removeHandler(handler) 

    MSG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    return logger
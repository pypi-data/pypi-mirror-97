import logging
from logging.handlers import RotatingFileHandler
from .slackNotifications import Slacker
import os

#_svc_name_ = "..."
#log_path = C:\\logs\\pythonservice\\

eformat = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(lineno)d %(message)s (in %(funcName)s)')
iformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s - (in %(funcName)s)')

def createLogger(name, log_path, level=logging.DEBUG, normal_format=iformat, error_format=eformat):
    handler = logging.FileHandler(os.path.join(log_path, 'info.log'))
    debug_handler = logging.FileHandler(
        os.path.join(log_path, 'debug.log'))
    error_handler = logging.FileHandler(
        os.path.join(log_path, 'error.log'))
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger


def createRotatingLogger(name, log_path, level=logging.DEBUG, normal_format = iformat, error_format = eformat):
    handler = RotatingFileHandler(os.path.join(log_path , 'info.log'),backupCount=20,maxBytes=10000000)
    debug_handler = RotatingFileHandler(os.path.join(log_path , 'debug.log'),backupCount=20,maxBytes=10000000)
    error_handler = RotatingFileHandler(os.path.join(log_path , 'error.log'),backupCount=20,maxBytes=10000000)
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger

def createSlackLogger(name, logger = None):
    slacker = Slacker()
    try:
        slacker.setup(name, logger=logger)
    except Exception as ex:
        print(ex)
    return slacker
import logging.handlers
import logging
import os
from config import Config
from base.singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self, dir_path=os.path.dirname(os.path.realpath(__file__))+os.path.sep):
        formatter = logging.Formatter('%(levelname)s %(asctime)s file %(filename)s linea %(lineno)d %(message)s')
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        if Config.getValue("loggingLevel") is not None:
            ch.setLevel(int(Config.getValue("loggingLevel")))
        ch.setFormatter(formatter)

        # create file handler and set level to debug
        fh = logging.handlers.TimedRotatingFileHandler(dir_path+'server.log', 'D')
        fh.setLevel(int(Config.getValue("loggingLevel")))
        fh.setFormatter(formatter)

        self.file_logger = logging.getLogger()
        self.file_logger.setLevel(int(Config.getValue("loggingLevel")))
        self.file_logger.addHandler(ch)
        self.file_logger.addHandler(fh)

    @staticmethod
    def getLogger():
        logger = Logger()
        return logger.file_logger


class LoggerClient(metaclass=Singleton):

    def __init__(self, dir_path=os.path.dirname(os.path.realpath(__file__))+os.path.sep):
        formatter = logging.Formatter('%(levelname)s %(asctime)s file %(filename)s linea %(lineno)d %(message)s')

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        if Config.getValue("loggingLevel") is not None:
            ch.setLevel(int(Config.getValue("loggingLevel")))
        ch.setFormatter(formatter)

        # create file handler and set level to debug
        fh = logging.handlers.TimedRotatingFileHandler(dir_path+'client.log', 'D')
        fh.setLevel(int(Config.getValue("loggingLevel")))
        fh.setFormatter(formatter)

        self.file_logger_client = logging.getLogger()
        self.file_logger_client.setLevel(int(Config.getValue("loggingLevel")))
        self.file_logger_client.addHandler(ch)
        self.file_logger_client.addHandler(fh)

    @staticmethod
    def getLogger():
        logger = LoggerClient()
        return logger.file_logger_client

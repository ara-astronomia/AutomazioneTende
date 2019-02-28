import logging.handlers
from config import Config
import os

class Logger:
    logger = None

    def __init__(self, dir_path=os.path.dirname(os.path.realpath(__file__))+os.path.sep):
        formatter = logging.Formatter('%(levelname)s %(asctime)s file %(filename)s linea %(lineno)d %(message)s')
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        if Config.getValue("loggingLevel") != None:
            ch.setLevel(int(Config.getValue("loggingLevel")))
        ch.setFormatter(formatter)

        # create file handler and set level to debug
        fh = logging.handlers.TimedRotatingFileHandler(dir_path+'automazione_tende.log', 'D')
        fh.setLevel(int(Config.getValue("loggingLevel")))
        fh.setFormatter(formatter)

        self.file_logger = logging.getLogger()
        self.file_logger.setLevel(int(Config.getValue("loggingLevel")))
        self.file_logger.addHandler(ch)
        self.file_logger.addHandler(fh)
        Logger.logger = self

    @staticmethod
    def getLogger():
        if Logger.logger is None:
            Logger.logger = Logger()
        return Logger.logger.file_logger

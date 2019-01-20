import configparser
import os

class Config:
    config = None

    def __init__(self, dir_path=os.path.dirname(os.path.realpath(__file__))+os.path.sep):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('config.ini')

    @staticmethod
    def getValue(key):
        if Config.config is None:
            Config.config = Config()
        try:
            return Config.config.configparser['automazione'][key]
        except KeyError:
            return None

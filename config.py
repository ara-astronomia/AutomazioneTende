import configparser
import os

class Config:
    config = None

    def __init__(self, dir_path=os.path.dirname(os.path.realpath(__file__))+os.path.sep):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('config.ini')

    @staticmethod
    def getValue(key, section='automazione'):
        if Config.config is None:
            Config.config = Config()
        return Config.config.configparser[section][key]

    @staticmethod
    def getFloat(key, section='automazione'):
        if Config.config is None:
            Config.config = Config()
        return Config.config.configparser[section].getfloat(key)

    @staticmethod
    def getInt(key, section='automazione'):
        if Config.config is None:
            Config.config = Config()
        return Config.config.configparser[section].getint(key)

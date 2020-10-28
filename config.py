import configparser
import os
from base.singleton import Singleton


class Config(metaclass=Singleton):

    def __init__(self):
        self.configparser = configparser.ConfigParser()
        configpath = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.configparser.read(configpath)

    @staticmethod
    def getValue(key, section='automazione'):
        config = Config()
        return config.configparser[section][key]

    @staticmethod
    def getFloat(key, section='automazione'):
        config = Config()
        return config.configparser[section].getfloat(key)

    @staticmethod
    def getInt(key, section='automazione'):
        config = Config()
        return config.configparser[section].getint(key)

    @staticmethod
    def setValue(key, section=''):
        config = Config()
        return config.configparser[section][key]

import configparser
from base.singleton import Singleton


class Config(metaclass=Singleton):

    def __init__(self):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('config.ini')

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

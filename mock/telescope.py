import configparser
import json
import os
import socket
from base import telescope
from logger import Logger
from status import TrackingStatus


class Telescope(telescope.BaseTelescope):

    def __init__(self):
        super().__init__()
        self.connected = False
        self.configparser = configparser.ConfigParser()

    def open_connection(self):
        self.connected = True

    def update_coords(self, **kwargs):
        alt = kwargs.get("alt")
        az = kwargs.get("az")
        tr = kwargs.get("tr")

        configpath = os.path.join(os.path.dirname(__file__), 'telescope.ini')
        self.configparser.read(configpath)

        if "coords" in self.configparser:
            if not self.__is_number__(alt, float, -90, 90):
                alt = self.configparser.getfloat("coords", "alt", fallback=0)
            if not self.__is_number__(az, float, 0, 360):
                az = self.configparser.getfloat("coords", "az", fallback=0)
            if not self.__is_number__(tr, int, 0, 1):
                tr = self.configparser.getint("coords", "tr", fallback=0)

        if not self.__is_number__(alt, float, -90, 90):
            alt = input("Inserisci l'altezza del telescopio: ")
        if not self.__is_number__(az, float, 0, 360):
            az = input("Inserisci l'azimut del telescopio: ")
        if not self.__is_number__(tr, int, 0, 1):
            tr = input("inserisci la situazione del tracking (1 o 0):")

        if not self.__is_number__(alt, float, -90, 90):
            print("Inserire un numero compreso tra 0 e 90 per l'altezza")
            return self.update_coords(az=kwargs.get("az"))
        if not self.__is_number__(az, float, 0, 360):
            print("Inserire un numero compreso tra 0 e 360 per l'azimut")
            return self.update_coords(alt=kwargs.get("alt"))
        if not self.__is_number__(tr, int, 0, 1):
            print("Inserire un numero compreso tra 1 o 0")
            return self.update_coords(alt=alt, az=az)

        self.coords = {'tr': int(tr), 'alt': round(float(alt)), 'az': round(float(az)), 'error': 0}

        config = configparser.ConfigParser()
        config["coords"] = {}
        config["coords"]["alt"] = str(alt)
        config["coords"]["az"] = str(az)
        config["coords"]["tr"] = str(tr)

        with open(configpath, 'w') as configfile:
            config.write(configfile)

        Logger.getLogger().debug("In update coords")
        return self.coords

    def move_tele(self, **kwargs):
        Logger.getLogger().debug("In park tele %s %s %s %s", kwargs.get("tr"), kwargs.get("alt"), kwargs.get("az"), self.max_secure_alt)
        self.update_coords(tr=kwargs.get("tr"), alt=kwargs.get("alt"), az=kwargs.get("az"))
        self.__update_status__()

    def flat_tele(self):
        Logger.getLogger().debug("In park tele %s %s %s", self.flat_alt, self.flat_az, self.max_secure_alt)
        return self.update_coords(alt=self.flat_alt, az=self.flat_az)

    def tele_tracking_on(self):
        pass

    def read(self):
        self.coords = self.update_coords()
        self.__update_status__()

    def __is_number__(self, s, kind=float, *args):
        if s is None:
            return False
        try:
            s = kind(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
        except (TypeError, ValueError):
            return False

        if args is not None:
            if len(args) == 2:
                return args[0] <= s <= args[1]

        return True

    def close_connection(self):
        self.connected = False

import socket, json
from base.base_telescopio import BaseTelescopio
from logger import Logger
from status import TrackingStatus

class Telescopio(BaseTelescopio):

    def __init__(self, hostname, script, script_park, script_flat, script_tracking_on, port: int = 3040):
        super().__init__()
        self.connected = False

    def open_connection(self):
        self.connected = True

    def update_coords(self, alt=None, az=None, tr=None):
        if not self.__is_number__(alt) or int(alt) < 0 or int(alt) > 90:
            alt = input("Inserisci l'altezza del telescopio: ")
        if not self.__is_number__(az) or int(az) < 0 or int(az) > 360:
            az = input("Inserisci l'azimut del telescopio: ")
        if not self.__is_number__(alt) or int(alt) < 0 or int(alt) > 90:
            print("Inserire un numero compreso tra 0 e 90 per l'altezza")
            return self.update_coords(az=az)
        if not self.__is_number__(az) or int(az) < 0 or int(az) > 360:
            print("Inserire un numero compreso tra 0 e 360 per l'azimut")
            return self.update_coords(alt=alt)
        if not self.__is_number__(tr) or int(tr) < 0 or int(tr) > 1:
            tr = input("inserisci la situazione del tracking (1 o 0):")
        if not self.__is_number__(tr) or int(tr) < 0 or int(tr) > 1:
            print("Inserire un numero compreso tra 1 o 0")
            return self.update_coords(alt=alt, az=az)
        self.coords = {'alt': int(alt), 'az': int(az), 'tr': int(tr), 'error': 0}
        Logger.getLogger().debug("In update coords")
        return self.coords

    def park_tele(self):
        Logger.getLogger().debug("In park tele %s %s %s", self.park_alt, self.park_az, self.max_secure_alt)
        self.update_coords(alt=self.park_alt, az=self.park_az)
        self.__update_status__()

    def flat_tele(self):
        Logger.getLogger().debug("In park tele %s %s %s", self.flat_alt, self.flat_az, self.max_secure_alt)
        self.update_coords(alt=self.flat_alt, az=self.flat_az, tr=0)
        self.__update_status__()

    def tele_tracking_on(self):
        self.update_coords(alt=self.flat_alt, az=self.flat_az, tr=1)
        self.__update_status__()

    def read(self):
        self.coords = self.update_coords()
        self.__update_status__()

    def __is_number__(self, s):
        if s is None:
            return False
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def close_connection(self):
        self.connected = False

import socket, json
from base.base_telescopio import BaseTelescopio
from logger import Logger

class Telescopio(BaseTelescopio):

    def __init__(self, hostname, script, script_park, script_flat, script_tracking_on, port: int = 3040):
        super().__init__()
        self.connected = False

    def open_connection(self):
        self.connected = True

    def update_coords(self, alt=None, az=None):
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
        self.coords = {'alt': int(alt), 'az': int(az), 'error': 0}
        Logger.getLogger().debug("In update coords")
        return self.coords

    def park_tele(self):
        Logger.getLogger().debug("In park tele %s %s %s", self.park_alt, self.park_az, self.max_secure_alt)
        return self.update_coords(alt=self.park_alt, az=self.park_az)

    def flat_tele(self):
        Logger.getLogger().debug("In park tele %s %s %s", self.flat_alt, self.flat_az, self.max_secure_alt)
        return self.update_coords(alt=self.flat_alt, az=self.flat_az)

    def tele_tracking_on(self):
        pass    

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

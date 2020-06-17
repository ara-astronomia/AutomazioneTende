import socket, json
from base.base_telescopio import BaseTelescopio
from logger import Logger
from status import TrackingStatus

class Telescopio(BaseTelescopio):

    def __init__(self):
        super().__init__()
        self.connected = False

    def open_connection(self):
        self.connected = True

    def update_coords(self, **kwargs):
        alt = kwargs.get("alt")
        az = kwargs.get("az")
        tr = kwargs.get("tr")
        if not self.__is_number__(alt) or float(alt) < 0 or float(alt) > 90:
            alt = input("Inserisci l'altezza del telescopio: ")
        if not self.__is_number__(az) or float(az) < 0 or float(az) > 360:
            az = input("Inserisci l'azimut del telescopio: ")
        if not self.__is_number__(alt) or float(alt) < 0 or float(alt) > 90:
            print("Inserire un numero compreso tra 0 e 90 per l'altezza")
            return self.update_coords(az=kwargs.get("az"))
        if not self.__is_number__(az) or float(az) < 0 or float(az) > 360:
            print("Inserire un numero compreso tra 0 e 360 per l'azimut")
            return self.update_coords(alt=kwargs.get("alt"))
        if not self.__is_number__(tr) or int(tr) < 0 or int(tr) > 1:
            tr = input("inserisci la situazione del tracking (1 o 0):")
        if not self.__is_number__(tr) or int(tr) < 0 or int(tr) > 1:
            print("Inserire un numero compreso tra 1 o 0")
            return self.update_coords(alt=alt, az=az)
        self.coords = {'tr': int(tr), 'alt': round(float(alt)), 'az': round(float(az)), 'error': 0}
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

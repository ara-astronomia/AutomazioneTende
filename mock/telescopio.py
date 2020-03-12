import socket,json
from base.base_telescopio import BaseTelescopio

class Telescopio(BaseTelescopio):

    def __init__(self, hostname, script, script_park, port: int = 3040):
        super().__init__()
        self.connected = False

    def open_connection(self):
        self.connected = True

    def update_coords(self, alt=None, az=None):
        if not alt or not az:
            alt = input("Inserisci l'altezza del telescopio: ")
            az = input("Inserisci l'azimut del telescopio: ")
        if not self.__is_number__(alt) or int(alt) < 0 or int(alt) > 90:
            print("Inserire un numero compreso tra 0 e 90 per l'altezza")
            return self.update_coords()
        if not self.__is_number__(az) or int(az) < 0 or int(az) > 360:
            print("Inserire un numero compreso tra 0 e 360 per l'azimut")
            return self.update_coords()
        self.coords = {'alt': int(alt), 'az': int(az)}
        return self.coords

    def park_tele(self):
        return self.update_coords(self.park_alt, self.park_azi)

    def __is_number__(self, s):
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

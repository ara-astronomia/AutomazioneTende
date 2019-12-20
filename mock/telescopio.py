import socket,json
from base.base_telescopio import BaseTelescopio

class Telescopio(BaseTelescopio):

    def __init__(self,hostname, port, script,script_park):
        pass

    def coords(self):
        alt = input("Inserisci l'altezza del telescopio: ")
        az = input("Inserisci l'azimut del telescopio: ")
        if not self.__is_number__(alt) or int(alt) < 0 or int(alt) > 90:
            print("Inserire un numero compreso tra 0 e 90 per l'altezza")
            return self.coords()
        if not self.__is_number__(az) or int(az) < 0 or int(az) > 360:
            print("Inserire un numero compreso tra 0 e 360 per l'azimut")
            return self.coords()
        return {'alt': int(alt), 'az': int(az)}

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


if __name__ == '__main__':
    netcat("192.168.0.9", 3040, 'MountGetAltAzi.js', 'SetParkTel.js')

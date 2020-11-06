import configparser
import datetime
import os
from components.telescope import telescope
from logger import Logger


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
        error = kwargs.get("error")

        configpath = os.path.join(os.path.dirname(__file__), 'telescope.ini')
        self.configparser.read(configpath)

        if "coords" in self.configparser:
            if not self.__is_number__(alt, float, -90, 90):
                alt = self.configparser.get("coords", "alt", fallback=0)
            if not self.__is_number__(az, float, 0, 360):
                az = self.configparser.get("coords", "az", fallback=0)
            if not self.__is_number__(tr):
                tr = self.configparser.get("coords", "tr", fallback=0)
            if not self.__is_number__(error, int, 0, 999):
                error = self.configparser.get("coords", "error", fallback=0)

        alt = self.__is_number_or_input__(alt, "l'altezza del telescopio", float, -90, 90)
        az = self.__is_number_or_input__(az, "l'azimut del telescopio", float, 0, 360)
        tr = self.__is_number_or_input__(tr, "la situazione del tracking")
        error = self.__is_number_or_input__(error, "il codice di errore (0 non ci sono errori)", int, 0, 999)

        self.coords = {'tr': tr, 'alt': round(alt, 2), 'az': round(az, 2), 'error': error}

        config = configparser.ConfigParser()
        config["coords"] = {'alt': str(alt), 'az': str(az), 'tr': str(tr), 'error': str(error)}

        with open(configpath, 'w') as configfile:
            config.write(configfile)

        Logger.getLogger().debug("In update coords %s", self.coords)
        return self.coords

    def move_tele(self, **kwargs):
        Logger.getLogger().debug("In park tele %s %s %s %s", kwargs.get("tr"), kwargs.get("alt"), kwargs.get("az"), self.max_secure_alt)
        self.update_coords(tr=kwargs.get("tr"), alt=kwargs.get("alt"), az=kwargs.get("az"))
        self.__update_status__()

    def read(self):
        self.coords = self.update_coords()
        self.__update_status__()

    def sync_tele(self, **kwargs):
        Logger.getLogger().debug("sincronizzo il telescopio a queste coordinate %s", kwargs)
        coords = self.radec2altaz(datetime.datetime.utcnow(), **kwargs)
        Logger.getLogger().debug("Coordinate %s %s", coords["alt"], coords["az"])
        self.update_coords(tr=1, alt=coords["alt"], az=coords["az"])
        return True

    def __is_number_or_input__(self, s, message, kind=int, start=0, stop=1):
        if self.__is_number__(s, kind, start, stop):
            return kind(s)

        s = input(f"Inserire un numero compreso tra {start} e {stop} per {message}: ")
        return self.__is_number_or_input__(s, message, kind, start, stop)

    def __is_number__(self, s, kind=int, start=0, stop=1):
        if s is None:
            return False
        try:
            s = kind(s)
        except ValueError:
            return False

        return start <= s <= stop

    def close_connection(self):
        self.connected = False

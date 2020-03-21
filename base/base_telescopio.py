import config
from enum import IntEnum, unique
from typing import Dict
from status import TelescopeStatus
from logger import Logger

class BaseTelescopio:

    def __init__(self):
        self.max_secure_alt: int = config.Config.getInt("max_secure_alt", "telescope")
        self.park_alt: int = config.Config.getInt("park_alt", "telescope")
        self.park_az: int = config.Config.getInt("park_az", "telescope")
        self.coords: Dict[str, int] = { "alt": 0, "az": 0, "error": 0 }
        self.status: TelescopeStatus = TelescopeStatus.PARKED

    def update_coords(self):
        raise NotImplementedError()

    def park_tele(self):
        raise NotImplementedError()

    def read(self, ):
        raise NotImplementedError()

    def __update_status__(self):
        if self.coords["error"]:
            self.status = TelescopeStatus.ERROR
            Logger.getLogger().error("Errore Telescopio: "+str(self.coords['error']))
        elif (
            self.coords["alt"] - 1 <= self.park_alt <= self.coords["alt"] + 1 and
            self.coords["az"] - 1 <= self.park_az <= self.coords["az"] + 1
        ):
            self.status = TelescopeStatus.PARKED
        elif self.coords["alt"] <= self.max_secure_alt:
            self.status = TelescopeStatus.SECURE
        else:
            self.status = TelescopeStatus.OPERATIONAL

        Logger.getLogger().debug("Altezza Telescopio: %s", str(self.coords['alt']))
        Logger.getLogger().debug("Azimut Telescopio: %s", str(self.coords['az']))
        Logger.getLogger().debug("Status Telescopio: %s", str(self.status))

        return self.status

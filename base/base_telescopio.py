import config
from enum import IntEnum, unique
from typing import Dict
from status import TelescopeStatus, TrackingStatus
from logger import Logger

class BaseTelescopio:

    def __init__(self):
        self.max_secure_alt: int = config.Config.getInt("max_secure_alt", "telescope")
        self.park_alt: int = config.Config.getInt("park_alt", "telescope")
        self.park_az: int = config.Config.getInt("park_az", "telescope")
        self.flat_alt: int = config.Config.getInt("flat_alt", "telescope")
        self.flat_az: int = config.Config.getInt("flat_az", "telescope")
        self.coords: Dict[str, int] = { "alt": 0, "az": 0, "tr" : 0, "error": 0 }
        self.status: TelescopeStatus = TelescopeStatus.PARKED
        self.tracking_status: TrackingStatus = TrackingStatus.OFF

    def update_coords(self):
        raise NotImplementedError()

    def park_tele(self):
        raise NotImplementedError()

    def flat_tele(self):
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
        elif (
            self.coords["alt"] -1 <= self.flat_alt <= self.coords["alt"] + 1 and
            self.coords["az"] -1 <= self.flat_az <= self.coords["az"] + 1
        ):
            self.status = TelescopeStatus.FLATTER
        elif self.coords["alt"] <= self.max_secure_alt:
            self.status = TelescopeStatus.SECURE
        else:
            self.status = TelescopeStatus.OPERATIONAL
        print (self.coords['tr'])
        if self.coords["tr"] == 0:
            self.tracking_status = TrackingStatus.OFF
        elif self.coords["tr"] == 1:
            self.tracking_status = TrackingStatus.ON


        Logger.getLogger().debug("Altezza Telescopio: %s", str(self.coords['alt']))
        Logger.getLogger().debug("Azimut Telescopio: %s", str(self.coords['az']))
        Logger.getLogger().debug("Status Telescopio: %s", str(self.status))
        Logger.getLogger().debug("Status Tracking: %s", str(self.coords['tr']))
        return self.status

import config
from enum import IntEnum, unique
from typing import Dict
from status import TelescopeStatus, TrackingStatus
from status import ButtonStatus
from status import SyncStatus
from logger import Logger
import components.telescope.sync
from components.telescope.sync import conv_altaz_to_ardec


class BaseTelescope:

    def __init__(self):
        self.max_secure_alt: int = config.Config.getFloat("max_secure_alt", "telescope")
        self.park_alt: int = config.Config.getFloat("park_alt", "telescope")
        self.park_az: int = config.Config.getFloat("park_az", "telescope")
        self.flat_alt: int = config.Config.getFloat("flat_alt", "telescope")
        self.flat_az: int = config.Config.getFloat("flat_az", "telescope")
        self.azimut_ne = config.Config.getInt("azNE", "azimut")
        self.azimut_se = config.Config.getInt("azSE", "azimut")
        self.azimut_sw = config.Config.getInt("azSW", "azimut")
        self.azimut_nw = config.Config.getInt("azNW", "azimut")
        self.coords: Dict[str, int] = {"alt": 0, "az": 0, "tr": 0, "error": 0}
        self.status: TelescopeStatus = TelescopeStatus.PARKED
        self.sync_status: SyncStatus = SyncStatus.OFF
        self.tracking_status: TrackingStatus = TrackingStatus.OFF
        # geographic SECTION
        """
        self.lat = config.Config.getValue("lat", "geographic")
        self.lon = config.Config.getValue("lon", "geographic")
        self.height = config.Config.getInt("height", "geographic")
        self.name_obs = config.Config.getValue("name_obs", "geographic")
        """
    def update_coords(self):
        raise NotImplementedError()

    def park_tele(self):
        raise NotImplementedError()

    def flat_tele(self):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def sync(self, sync_time):
        utc_now = sync_time
        data = conv_altaz_to_ardec(utc_now)
        Logger.getLogger().debug("tempo UTC di sync in telescope.theskyx.telescope: %s", utc_now)
        data = {"ar": data[0], "dec": data[1]}
        Logger.getLogger().debug("valori di sincronizzazione diar e dec al tempo UTC di sync: %s", data)
        if self.sync_tele(**data):
            self.sync_status = SyncStatus.ON
        else:
            self.sync_status = SyncStatus.OFF

    def nosync(self):
        self.sync_status: SyncStatus = SyncStatus.OFF

    def __update_status__(self):

        if self.coords["error"]:
            self.status = TelescopeStatus.ERROR
            Logger.getLogger().error("Errore Telescopio: "+str(self.coords['error']))
        elif self.__within_park_alt_range__() and self.__within_park_az_range__():
            self.status = TelescopeStatus.PARKED
        elif self.__within_flat_alt_range__() and self.__within_flat_az_range__():
            self.status = TelescopeStatus.FLATTER
        elif self.coords["alt"] <= self.max_secure_alt:
            self.status = TelescopeStatus.SECURE
        else:
            if self.azimut_ne > self.coords['az']:
                self.status = TelescopeStatus.NORTHEAST
            elif self.coords['az'] > self.azimut_nw:
                self.status = TelescopeStatus.NORTHWEST
            elif self.azimut_sw > self.coords['az'] > 180:
                self.status = TelescopeStatus.SOUTHWEST
            elif 180 >= self.coords['az'] > self.azimut_se:
                self.status = TelescopeStatus.SOUTHEAST
            elif self.azimut_sw < self.coords["az"] <= self.azimut_nw:
                self.status = TelescopeStatus.WEST
            elif self.azimut_ne <= self.coords["az"] <= self.azimut_se:
                self.status = TelescopeStatus.EAST

        self.tracking_status = TrackingStatus.from_value(self.coords["tr"])

        Logger.getLogger().debug("Altezza Telescopio: %s", str(self.coords['alt']))
        Logger.getLogger().debug("Azimut Telescopio: %s", str(self.coords['az']))
        Logger.getLogger().debug("Status Telescopio: %s", str(self.status))
        Logger.getLogger().debug("Status Tracking: %s %s", str(self.coords['tr']), str(self.tracking_status))
        Logger.getLogger().debug("Status Sync: %s ", str(self.sync_status))
        return self.status

    def is_within_curtains_area(self):
        return self.status in [
            TelescopeStatus.EAST,
            TelescopeStatus.WEST
        ]

    def update_status_sync(self):
        self.sync_status = SyncStatus.ON

    def is_below_curtains_area(self):
        return self.coords["alt"] <= self.max_secure_alt

    def is_above_curtains_area(self, max_est, max_west):
        return self.coords["alt"] >= max_est and self.coords["alt"] >= max_west

    def __within_flat_alt_range__(self):
        return self.__within_range__(self.coords["alt"], self.flat_alt)

    def __within_park_alt_range__(self):
        return self.__within_range__(self.coords["alt"], self.park_alt)

    def __within_flat_az_range__(self):
        return self.__within_range__(self.coords["az"], self.flat_az)

    def __within_park_az_range__(self):
        return self.__within_range__(self.coords["az"], self.park_az)

    def __within_range__(self, coord, check):
        return coord - 1 <= check <= coord + 1

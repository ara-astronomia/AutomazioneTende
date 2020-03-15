import config
from enum import IntEnum, unique
from typing import Dict
from status import TelescopeStatus
from orientation import Orientation

class BaseTelescopio:

    def __init__(self):
        self.max_secure_alt: int = config.Config.getInt("max_secure_alt", "telescope")
        self.park_alt: int = config.Config.getInt("park_alt", "telescope")
        self.park_azi: int = config.Config.getInt("park_azi", "telescope")
        self.coords: Dict[str, int] = { "alt": 0, "az": 0 }

    def update_coords(self):
        raise NotImplementedError()

    def park_tele(self):
        raise NotImplementedError()

    def read(self, update=False):
        if update:
            self.coords = self.update_coords() # is it really necessary?

        if (
            self.coords["alt"] - 1 <= self.park_alt <= self.coords["alt"] + 1 and 
            self.coords["az"] - 1 <= self.park_azi <= self.coords["az"] + 1
           ):
            return TelescopeStatus.PARKED
        elif self.coords["alt"] <= self.max_secure_alt:
            return TelescopeStatus.SECURE
        else:
            return TelescopeStatus.OPERATIONAL

    def orientation(self):
        return Orientation.EAST if 0 >= self.coords["azi"] > 180 else Orientation.WEST

import config
from enum import IntEnum, unique
from typing import Dict
from status import TelescopeStatus

class BaseTelescopio:

    def __init__(self):
        self.max_secure_alt = config.Config.getInt("max_secure_alt", "telescope")
        self.park_alt = config.Config.getInt("park_alt", "telescope")
        self.park_azi = config.Config.getInt("park_azi", "telescope")
        self.coords: Dict[str, int] = { "alt": 0, "az": 0 }

    def update_coords(self):
        raise NotImplementedError()

    def park_tele(self):
        raise NotImplementedError()

    def read(self, update=False):
        if update:
            self.coords = self.update_coords() # is it really necessary?

        if self.coords["alt"] == self.park_alt and self.coords["az"] == self.park_azi:
            return TelescopeStatus.PARKED
        elif self.coords["alt"] <= self.max_secure_alt:
            return TelescopeStatus.SECURE
        else:
            return TelescopeStatus.OPERATIONAL

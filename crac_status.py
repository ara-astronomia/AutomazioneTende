from typing import Dict
from typing import SupportsRound
from status import Status
from status import CurtainsStatus
from status import TelescopeStatus
from status import ButtonStatus
from status import TrackingStatus
from status import SyncStatus
from status import SlewingStatus

from logger import Logger
APP = "SERVER"


def init():
    global APP
    if APP == "SERVER":
        from logger import Logger
    else:
        from logger import LoggerClient as Logger


def __convert_steps__(steps: SupportsRound) -> str:
    return f'{round(steps):03}'


def __convert_coords__(coords: Dict[str, float]) -> str:
    alt = int(coords["alt"] * 100)
    if alt > 9000:
        ValueError("Altezza telescopio non valida")
    az = int(coords["az"] * 100)
    if az > 36000:
        ValueError("Azimut telescopio non valido")
    Logger.getLogger().debug("converted coords VALUE: %s", f'{alt:05}{az:05}')
    return f'{alt:05}{az:05}'


def __reverse_coords__(value: str) -> Dict:
    alt = round(float(f"{value[0:3]}.{value[3:5]}"), 2)
    az = round(float(f"{value[5:8]}.{value[8:10]}"), 2)
    coords = {"alt": alt, "az": az}
    Logger.getLogger().debug("coords VALUE: %s", coords)
    return coords


def __structure__():
    status = Status.CLOSED
    parked = TelescopeStatus.PARKED
    coords = {"alt": 0.00, "az": 0.00}
    disabled = CurtainsStatus.DISABLED
    tracking = TrackingStatus.OFF
    slewing = SlewingStatus.OFF
    button = ButtonStatus.OFF
    sync = SyncStatus.OFF

    data = {}
    data["roof_status"] = {"orig": status, "trans": repr, "reverse": status.get_value}
    data["telescope_status"] = {"orig": parked, "trans": repr, "reverse": parked.get_value}
    data["telescope_coords"] = {"len": 10, "orig": coords, "trans": __convert_coords__, "reverse": __reverse_coords__}
    data["curtain_east_status"] = {"orig": disabled, "trans": repr, "reverse": disabled.get_value}
    data["curtain_east_steps"] = {"orig": 0, "trans": __convert_steps__, "reverse": int}
    data["curtain_west_status"] = {"orig": disabled, "trans": repr, "reverse": disabled.get_value}
    data["curtain_west_steps"] = {"orig": 0, "trans": __convert_steps__, "reverse": int}
    data["tracking_status"] = {"orig": tracking, "trans": repr, "reverse": tracking.get_value}
    data["panel_status"] = {"orig": button, "trans": repr, "reverse": button.get_value}
    data["power_tele_status"] = {"orig": button, "trans": repr, "reverse": button.get_value}
    data["light_status"] = {"orig": button, "trans": repr, "reverse": button.get_value}
    data["power_ccd_status"] = {"orig": button, "trans": repr, "reverse": button.get_value}
    data["sync_status"] = {"orig": sync, "trans": repr, "reverse": sync.get_value}
    data["slewing_status"] = {"orig": slewing, "trans": repr, "reverse": slewing.get_value}
    return data


class CracStatus:

    _structure = __structure__()

    def __init__(self, code: str = None):
        self.logger = Logger.getLogger()

        self.length = 0
        if not code:
            for key, value in self._structure.items():
                default_value = value["orig"]
                self.__dict__[f"_{key}"] = default_value
                self.length += len(value["trans"](default_value))
        else:
            self.update(code)
    
    def update(self, code: str):
        i = 0
        for key, value in self._structure.items():
            default_value = value["trans"](value["orig"])
            length = len(default_value)
            end = i + length
            self.logger.debug("%s code VALUE: %s", key, code[i:end])
            self.logger.debug("%s length VALUE: %s", key, length)
            self.__reverse__(code[i:end], key)
            self.length += length
            i = end

    def __repr__(self):
        code = ""
        for key, value in self._structure.items():
            code += value["trans"](self.__dict__[f"_{key}"])
        self.logger.debug("FULL CODE VALUE: %s", code)
        return code

    def __check_type__(self, value, name):
        kind = type(self._structure[name]["orig"])
        if not isinstance(value, kind):
            raise ValueError(f"{name} should be of type {kind} but was {value}")

    def __convert__(self, value, name):
        self.__check_type__(value, name)
        self.__dict__[f"_{name}"] = self._structure[name]["trans"](value)

    def __assign__(self, value, name):
        self.__check_type__(value, name)
        if self.__dict__[f"_{name}"] != value:
            self.__dict__[f"_{name}_changed"] = True
        else:
            self.__dict__[f"_{name}_changed"] = False
        self.__dict__[f"_{name}"] = value

    def __reverse__(self, value, name):
        reverse = self._structure[name]["reverse"]
        self.__assign__(reverse(value), name)

    @property
    def roof_status(self):
        return self._roof_status

    @roof_status.setter
    def roof_status(self, value):
        self.__assign__(value, "roof_status")

    @property
    def telescope_status(self):
        return self._telescope_status

    @telescope_status.setter
    def telescope_status(self, value):
        self.__assign__(value, "telescope_status")

    @property
    def telescope_coords(self):
        return self._telescope_coords

    @telescope_coords.setter
    def telescope_coords(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "telescope_coords")

    @property
    def curtain_east_status(self):
        return self._curtain_east_status

    @curtain_east_status.setter
    def curtain_east_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "curtain_east_status")

    @property
    def curtain_east_steps(self):
        return self._curtain_east_steps

    @curtain_east_steps.setter
    def curtain_east_steps(self, value: int) -> None:
        self.__assign__(value, "curtain_east_steps")

    @property
    def curtain_west_status(self):
        return self._curtain_west_status

    @curtain_west_status.setter
    def curtain_west_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "curtain_west_status")

    @property
    def curtain_west_steps(self):
        return self._curtain_west_steps

    @curtain_west_steps.setter
    def curtain_west_steps(self, value: int) -> None:
        self.__assign__(value, "curtain_west_steps")

    @property
    def tracking_status(self):
        return self._tracking_status

    @tracking_status.setter
    def tracking_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "tracking_status")

    @property
    def slewing_status(self):
        return self._slewing_status

    @slewing_status.setter
    def slewing_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "slewing_status")

    @property
    def sync_status(self):
        return self._sync_status

    @sync_status.setter
    def sync_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "sync_status")

    @property
    def panel_status(self):
        return self._panel_status

    @panel_status.setter
    def panel_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "panel_status")

    @property
    def power_tele_status(self):
        return self._power_tele_status

    @power_tele_status.setter
    def power_tele_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "power_tele_status")

    @property
    def light_status(self):
        return self._light_status

    @light_status.setter
    def light_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "light_status")

    @property
    def power_ccd_status(self):
        return self._power_ccd_status

    @power_ccd_status.setter
    def power_ccd_status(self, value: Dict[str, int]) -> None:
        self.__assign__(value, "power_ccd_status")

    def are_curtains_disabled(self):
        return self.curtain_east_status is CurtainsStatus.DISABLED and self.curtain_west_status is CurtainsStatus.DISABLED

    def are_curtains_in_danger(self):
        return self.curtain_east_status is CurtainsStatus.DANGER or self.curtain_west_status is CurtainsStatus.DANGER

    def is_in_anomaly(self):
        self.logger.debug("roof status %s", self.roof_status)
        self.logger.debug("telescope status %s", self.telescope_status)
        self.logger.debug("curtain east status %s", self.curtain_east_status)
        self.logger.debug("curtain west status %s", self.curtain_west_status)

        return (
                    self.roof_status is Status.CLOSED and
                    (
                        self.curtain_east_status > CurtainsStatus.DISABLED or
                        self.curtain_west_status > CurtainsStatus.DISABLED or
                        self.telescope_status > TelescopeStatus.SECURE
                    )
                )

    def telescope_in_secure_and_roof_is_closed(self):
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSED

    def telescope_in_secure_and_roof_is_closing(self):
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSING


if __name__ == "__main__":
    cs = CracStatus()
    cs.curtain_east_status = CurtainsStatus.STOPPED
    print(cs.roof_status)
    print(cs.telescope_status)
    print(cs.telescope_coords)
    print(cs.sync_status)
    print(cs.curtain_east_status)
    print(cs.curtain_east_steps)
    print(cs.curtain_west_status)
    print(cs.curtain_west_steps)
    print(cs.tracking_status)
    print(cs.slewing_status)
    print(cs.panel_status)
    print(cs.power_tele_status)
    print(cs.light_status)
    print(cs.power_ccd_status)
    print(cs.length)
    cs = CracStatus("CPP100012045D000D000TNSSSS")
    print(cs.roof_status)
    print(cs.telescope_status)
    print(cs.telescope_coords)
    print(cs.sync_status)
    print(cs.curtain_east_status)
    print(cs.curtain_east_steps)
    print(cs.curtain_west_status)
    print(cs.curtain_west_steps)
    print(cs.tracking_status)
    print(cs.slewing_status)
    print(cs.panel_status)
    print(cs.power_tele_status)
    print(cs.light_status)
    print(cs.power_ccd_status)
    print(cs.length)

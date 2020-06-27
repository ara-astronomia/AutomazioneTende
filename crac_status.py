from typing import Dict
from status import Status
from status import TelescopeStatus
from status import ButtonStatus
from status import TrackingStatus

from logger import Logger
APP = "SERVER"


def init():
    global APP


class CracStatus():

    def __init__(self, code: str = None):
        if APP == "SERVER":
            from logger import Logger
        else:
            from logger import LoggerClient as Logger

        self.logger = Logger.getLogger()

        if not code:
            self.roof_status: Status = Status.CLOSED
            self.telescope_status: TelescopeStatus = TelescopeStatus.PARKED
            self._telescope_coords: Dict[str, str] = {"alt": "000", "az": "000"}
            self.curtain_east_status: Status = Status.STOPPED
            self._curtain_east_steps: str = "000"
            self.curtain_west_status: Status = Status.STOPPED
            self._curtain_west_steps: str = "000"
            self.tracking_status: TrackingStatus = TrackingStatus.OFF
            self.panel_status: ButtonStatus = ButtonStatus.OFF
            self.power_status: ButtonStatus = ButtonStatus.OFF
            self.light_status: ButtonStatus = ButtonStatus.OFF
            self.aux_status: ButtonStatus = ButtonStatus.OFF

        elif len(code) == 22:
            self.roof_status = Status.get_value(code[0])
            self.telescope_status = TelescopeStatus.get_value(code[1:3])
            self._telescope_coords = {"alt": code[3:6], "az": code[6:9]}
            self.curtain_east_status = Status.get_value(code[9])
            self._curtain_east_steps = code[10:13]
            self.curtain_west_status = Status.get_value(code[13])
            self._curtain_west_steps = code[14:17]
            self.tracking_status = TrackingStatus.get_value(code[17])
            self.panel_status = ButtonStatus.get_value(code[18])
            self.power_status = ButtonStatus.get_value(code[19])
            self.light_status = ButtonStatus.get_value(code[20])
            self.aux_status = ButtonStatus.get_value(code[21])

        elif len(code) == 3:
            self.roof_status = Status.get_value(code[0])
            self.curtain_west_status = Status.get_value(code[1])
            self.curtain_east_status = Status.get_value(code[2])
            self.telescope_status: TelescopeStatus = TelescopeStatus.PARKED
            self._telescope_coords: Dict[str, str] = {"alt": "000", "az": "000"}
            self._curtain_east_steps: str = "000"
            self._curtain_west_steps: str = "000"

    def __repr__(self):
        return f'{repr(self.roof_status)}{repr(self.telescope_status)}{self.telescope_coords["alt"]}{self.telescope_coords["az"]}{repr(self.curtain_east_status)}{self.curtain_east_steps}{repr(self.curtain_west_status)}{self.curtain_west_steps}{repr(self.tracking_status)}{repr(self.panel_status)}{repr(self.power_status)}{repr(self.light_status)}{repr(self.aux_status)}'

    @property
    def telescope_coords(self):
        return self._telescope_coords

    @telescope_coords.setter
    def telescope_coords(self, coords: Dict[str, int]) -> None:
        self._telescope_coords = {"alt": self.__convert_steps__(coords["alt"]), "az": self.__convert_steps__(coords["az"])}

    @property
    def curtain_east_steps(self) -> str:
        return self._curtain_east_steps

    @curtain_east_steps.setter
    def curtain_east_steps(self, steps: int) -> None:
        self._curtain_east_steps = self.__convert_steps__(steps)

    @property
    def curtain_west_steps(self) -> str:
        return self._curtain_west_steps

    @curtain_west_steps.setter
    def curtain_west_steps(self, steps: int) -> None:
        self._curtain_west_steps = self.__convert_steps__(steps)

    def __convert_steps__(self, steps: int) -> str:
        return f'{steps:03}'

    def are_curtains_closed(self):
        self.logger.debug("curtain east status %s", self.curtain_east_status)
        self.logger.debug("curtain west status %s", self.curtain_west_status)
        return self.curtain_east_status is Status.CLOSED and self.curtain_west_status is Status.CLOSED

    def are_curtains_in_danger(self):
        self.logger.debug("curtain east status %s", self.curtain_east_status)
        self.logger.debug("curtain west status %s", self.curtain_west_status)
        return self.curtain_east_status is Status.DANGER or self.curtain_west_status is Status.DANGER

    def is_in_anomaly(self):
        self.logger.debug("telescope status %s", self.telescope_status)
        self.logger.debug("curtain east status %s", self.curtain_east_status)
        self.logger.debug("curtain west status %s", self.curtain_west_status)
        return (
                    self.roof_status is Status.CLOSED and
                    (
                        self.curtain_east_status > Status.CLOSED or
                        self.curtain_west_status > Status.CLOSED or
                        self.telescope_status > TelescopeStatus.SECURE
                    )
                )

    def telescope_in_secure_and_roof_is_closed(self):
        self.logger.debug("telescope status %s", self.telescope_status)
        self.logger.debug("roof status %s", self.roof_status)
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSED

    def telescope_in_secure_and_roof_is_closing(self):
        self.logger.debug("telescope status %s", self.telescope_status)
        self.logger.debug("roof status %s", self.roof_status)
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSING

    def lenght(self):
        return len(repr(self))

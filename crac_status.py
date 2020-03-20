from status import Status, TelescopeStatus
from typing import Dict
from logger import Logger

class CracStatus():

    def __init__(self, code: str = None):
        self.roof_status: Status = Status.CLOSED
        self.telescope_status: TelescopeStatus = TelescopeStatus.PARKED
        self._telescope_coords: Dict[str, str] = { "alt": "000", "az": "000" }
        self.curtain_east_status: Status = Status.CLOSED
        self._curtain_east_steps: str = "000"
        self.curtain_west_status: Status = Status.CLOSED
        self._curtain_west_steps: str = "000"
        
        if code:
            self.roof_status = Status.get_value(code[0])
            self.telescope_status = TelescopeStatus.get_value(code[1])
            self._telescope_coords = { "alt": code[2:5], "az": code[5:8] }
            self.curtain_east_status = Status.get_value(code[8])
            self._curtain_east_steps = code[9:12]
            self.curtain_west_status = Status.get_value(code[12])
            self._curtain_west_steps = code[13:16]

    def __repr__(self):
        return f'{repr(self.roof_status)}{repr(self.telescope_status)}{self.telescope_coords["alt"]}{self.telescope_coords["az"]}{repr(self.curtain_east_status)}{self.curtain_east_steps}{repr(self.curtain_west_status)}{self.curtain_west_steps}'

    @property
    def telescope_coords(self):
        return self._telescope_coords
    
    @telescope_coords.setter
    def telescope_coords(self, coords: Dict[str, int]) -> None:
        self._telescope_coords = { "alt": self.__convert_steps__(coords["alt"]), "az": self.__convert_steps__(coords["az"]) }

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
        return self.curtain_east_status is Status.CLOSED and self.curtain_west_status is Status.CLOSED

    def are_curtains_in_danger(self):
        return self.curtain_east_status is Status.DANGER or self.curtain_west_status is Status.DANGER

    def is_in_anomaly(self):
        return (
                    self.roof_status is Status.CLOSED and 
                    (
                        self.curtain_east_status > Status.CLOSED or
                        self.curtain_west_status > Status.CLOSED or
                        self.telescope_status > TelescopeStatus.SECURE
                    )
                )
    
    def telescope_in_secure_and_roof_is_closed(self):
        Logger.getLogger().info("telescope_in_secure %s", self.telescope_status > TelescopeStatus.PARKED)
        Logger.getLogger().info("roof_is_closed %s", self.roof_status is Status.CLOSED)
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSED
    
    def telescope_in_secure_and_roof_is_closing(self):
        return self.telescope_status > TelescopeStatus.PARKED and self.roof_status is Status.CLOSING
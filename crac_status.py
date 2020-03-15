from status import Status, TelescopeStatus
from typing import Dict

class CracStatus():

    def __init__(self, code: str = None):
        self.roof_status: Status = Status.CLOSED
        self.telescope_status: TelescopeStatus = TelescopeStatus.PARKED
        self.telescope_coords: Dict[str, int] = { "alt": 0, "az": 0 }
        self.old_telescope_coords: Dict[str, int] = { "alt": 0, "az": 0 }
        self.curtain_east_status: Status = Status.CLOSED
        self.curtain_east_steps: int = 0
        self.old_curtain_east_steps: int = 0
        self.curtain_west_status: Status = Status.CLOSED
        self.curtain_west_steps: int = 0
        self.old_curtain_west_steps: int = 0
        
        if code:
            self.roof_status = Status.get_value(code[0])
            self.telescope_status = TelescopeStatus.get_value(code[1])
            self.telescope_coords = { "alt": int(code[2:5]), "az": int(code[5:8]) }
            self.curtain_east_status = Status.get_value(code[8])
            self.curtain_east_steps = int(code[9:12])
            self.curtain_west_status = Status.get_value(code[12])
            self.curtain_west_steps = int(code[13:16])

    def __repr__(self):
        return f'{repr(self.roof_status)}{repr(self.telescope_status)}{self.__repr_telescope_coords__(self.telescope_coords)}{repr(self.curtain_east_status)}{self.__convert_repr__(self.curtain_east_steps)}{repr(self.curtain_west_status)}{self.__convert_repr__(self.curtain_west_steps)}'

    def __repr_telescope_coords__(self, coords: Dict[str, int]) -> str:
        return self.__convert_repr__(coords["alt"]) + self.__convert_repr__(coords["az"])

    def __convert_repr__(self, steps: int) -> str:
        return f'{steps:03}'

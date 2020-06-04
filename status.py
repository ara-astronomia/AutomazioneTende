from enum import Enum, unique

class OrderedEnum(Enum):

    def __init__(self, value: int, abbr: str):
        self._value_ = value
        self.abbr = abbr

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
          return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
           return self.value < other.value
        return NotImplemented

    def __repr__(self):
        return self.abbr

    @classmethod
    def get_value(cls, abbr):
        for member in cls:
            if member.abbr == abbr:
                return member
        return None

@unique
class Status(OrderedEnum):

    # static statuses have lower values
    CLOSED = (1, "C")
    STOPPED = (2, "S")
    OPEN = (3, "O")

    # movement statuses have higher values
    CLOSING = (4, "L")
    OPENING = (5, "P")

    # danger zone - threat it as a movement statuses (but we hope it has stopped)
    # user should manually reset the steps after checking visually the curtains status
    DANGER = (6, "D")
    ERROR = (7, "E")

@unique
class TelescopeStatus(OrderedEnum):

    PARKED = (0, "P") #TELESCOPIO IN PARK
    SECURE = (1, "S") #TELESCOPIO IN SICUREZZA, SOTTO IL COLMO DEL TETTO
    OPERATIONAL = (2, "O") #TELESCOPIO IN CONDIZIONE DI OPERABILITÀ
    FLATTER = (5, "F") #TELESCOPIO IN POSIZIONE DI RIPRESA FLAT

    # danger zone - threat it as an operational status (but we hope it has stopped)
    # user should manually reset the steps after checking visually the curtains status
    LOST = (3, "L")
    ERROR = (4, "E")

@unique
class PanelStatus(OrderedEnum):

    OFF = (0, "S") #PANNELLO FLAT SPENTO
    ON = (1, "A") #PANNELLO FLAT ACCESO

@unique
class TrackingStatus(OrderedEnum):
    OFF = (0, "T") #VELOCITÀ TERRESTRE
    ON = (1, "S") #VELOCITÀ SIDERALE

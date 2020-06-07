import socket, json, re
from base.base_telescopio import BaseTelescopio
from logger import Logger
from typing import Dict
from status import TelescopeStatus

class Telescopio(BaseTelescopio):

    def __init__(self, hostname: str, script: str, script_park: str, script_flat: str, script_tracking_on: str, port: int=3040):
        super().__init__()
        self.hostname = hostname
        self.port: int = port
        self.script: str = script
        self.script_park: str = script_park
        self.script_flat: str = script_flat
        self.script_tracking_on: str = script_tracking_on
        self.connected: bool = False

    def open_connection(self) -> None:

        if not self.connected:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.hostname, self.port))
            self.connected = True

    def update_coords(self) -> Dict[str, int]:
        Logger.getLogger().info("Leggo le coordinate")
        data = self.__call_thesky__(self.script)
        Logger.getLogger().debug("Coordinate lette")
        self.__parse_result__(data.decode("utf-8"))
        return self.coords

    def park_tele(self) -> Dict[str, int]:
        Logger.getLogger().info("metto in park il telescopio")
        data = self.__call_thesky__(self.script_park, 0.2, 0.1, 0)
        Logger.getLogger().debug("Parking %s", data)
        self.coords["error"] = self.__is_error__(data.decode("utf-8"))
        self.__update_status__()
        #if self.read() != TelescopeStatus.PARKED:
            # recursive workaround in the case the park can't stop the sidereal movement.
            # return self.park_tele()
        self.coords

    def flat_tele(self) -> Dict[str, int]:
        Logger.getLogger().info("metto il telescopio in posizione di flat")
        data = self.__call_thesky__(self.script_park, 0.5, 2, 0)
        Logger.getLogger().debug("Flatter %s", data)
        self.coords["error"] = self.__is_error__(data.decode("utf-8"))
        self.__update_status__()
        #if self.read() != TelescopeStatus.FLATTER:
            # recursive workaround in the case the flatted can't stop the sidereal movement.
            # return self.park_tele()
        self.coords

    def tele_tracking_on(self) -> Dict[str, int]:
        Logger.getLogger().info("metto il telescopio in tracking on")
        data = self.__call_thesky__(self.script_park, "null", "null", 1)
        Logger.getLogger().debug("tele in tracking on")
        self.coords["error"] = self.__is_error__(data.decode("utf-8"))
        self.__update_status__()
        #if self.read() != TelescopeStatus.FLATTER:
            # recursive workaround in the case the flatted can't stop the sidereal movement.
            # return self.park_tele()
        self.coords

    def read(self, ):
        try:
            self.coords = self.update_coords() # is it really necessary?
        except (ConnectionError, TimeoutError):
            Logger.getLogger().exception("Connessione con The Sky persa: ")
            self.status = TelescopeStatus.LOST
        else:
            self.__update_status__()

    def __call_thesky__(self, script: str, alt: float = None, az: float = None, tr: int = None) -> bytes:
#        self.open_connection()
        with open(script, 'r') as p:
            file = p.read()
            self.s.sendall(file.format(az=az, alt=alt, tr=tr).encode('utf-8'))
            Logger.getLogger().debug("file inviato")
            data = self.s.recv(1024)
            print(str(data) + "questi sono i dati letti dal file js")
            Logger.getLogger().debug(data)
#        self.close_connection()
        return data

    def __parse_result__(self, data: str):

        self.coords["error"] = self.__is_error__(data)

        if not self.coords["error"]:
            jsonStringEnd = data.find("|")
            jsonString = data[:jsonStringEnd]
            coords = json.loads(jsonString)
            self.coords["alt"] = int(round(coords["alt"]))
            self.coords["az"] = int(round(coords["az"]))
            self.coords["tr"] =  int(round(coords["tr"]))
        Logger.getLogger().debug("Coords Telescopio: %s", str(self.coords))


    def __is_error__(self, input_str, search_reg="Error = ([1-9][^\\d]|\\d{2,})") -> int:
        r = re.search(search_reg, input_str)
        error_code = 0
        if r:
            r2 = re.search('\\d+', r.group(1))
            if r2:
                error_code = int(r2.group(0))
        return error_code

    def close_connection(self) -> None:
        if self.connected:
            self.s.close()
            self.connected = False

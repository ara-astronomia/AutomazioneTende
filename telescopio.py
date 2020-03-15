import socket,json
from base.base_telescopio import BaseTelescopio
from logger import Logger
from typing import Dict
from status import TelescopeStatus

class Telescopio(BaseTelescopio):

    def __init__(self, hostname: str, script: str, script_park: str, port: int=3040):
        super().__init__()
        self.hostname = hostname
        self.port: int = port
        self.script: str = script
        self.script_park: str = script_park
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
        return self.__parse_result__(data.decode("utf-8"))

    def park_tele(self) -> Dict[str, int]:
        Logger.getLogger().info("metto in park il telescopio")
        self.__call_thesky__(self.script_park)
        Logger.getLogger().debug("Telescopio inviato alla posizione di park")
        if self.read(update=True) != TelescopeStatus.PARKED:
            # recursive workaround in the case the park can't stop the sidereal movement.
            return self.park_tele()
        return self.coords

    def __call_thesky__(self, script: str) -> bytes:
        with open(script, 'r') as p:
            file = p.read().encode('utf-8')
            self.s.sendall(file)
            Logger.getLogger().info("file inviato")
            data = self.s.recv(1024)
            Logger.getLogger().info(data)
            return data

    def __parse_result__(self, data: str) -> Dict[str, int]:
        error = data.find("No error") == -1 or data.find('undefined') > -1
        Logger.getLogger().debug("Errore Telescopio: "+str(error))
        if error:
            jsonString = '{"error": true}'
            coords = json.loads(jsonString)
        else:
            jsonStringEnd = data.find("|")
            jsonString = data[:jsonStringEnd]
            coords = json.loads(jsonString)
            coords["alt"] = int(round(coords["alt"]))
            coords["az"] = int(round(coords["az"]))
        Logger.getLogger().debug("Coords Telescopio: "+str(coords))
        return coords

    def close_connection(self) -> None:
        if self.connected:
            self.s.close()
            self.connected = False

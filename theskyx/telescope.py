import json
import re
import socket
import config
from base.telescope import BaseTelescope
from logger import Logger
from typing import Dict
from status import TelescopeStatus


class Telescope(BaseTelescope):

    def __init__(self):
        super().__init__()
        self.hostname = config.Config.getValue("theskyx_server")
        self.port: int = 3040
        self.script: str = config.Config.getValue('altaz_mount_file')
        self.script_move_track: str = config.Config.getValue('move_track_tele_file')
        self.connected: bool = False

    def open_connection(self) -> None:

        if not self.connected:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.hostname, self.port))
            self.connected = True

    def update_coords(self) -> Dict[str, int]:
        Logger.getLogger().info("Leggo le coordinate")
        data = self.__call_thesky__(self.script)
        Logger.getLogger().debug("Coordinate lette: %s", data)
        self.__parse_result__(data.decode("utf-8"))
        return self.coords

    def move_tele(self, **kwargs) -> Dict[str, int]:
        Logger.getLogger().info("metto in park il telescopio")
        data = self.__call_thesky__(script=self.script_move_track, **kwargs)
        Logger.getLogger().debug("Parking %s", data)
        self.coords["error"] = self.__is_error__(data.decode("utf-8"))
        self.__update_status__()
        self.coords

    def read(self):
        try:
            self.update_coords()
        except (ConnectionError, TimeoutError):
            Logger.getLogger().exception("Connessione con The Sky persa: ")
            self.status = TelescopeStatus.LOST
        else:
            self.__update_status__()

    def __call_thesky__(self, script: str, **kwargs) -> bytes:
        self.open_connection()
        with open(script, 'r') as p:
            file = p.read()
            if kwargs:
                if kwargs.get("az") is None:
                    kwargs["az"] = ""
                if kwargs.get("alt") is None:
                    kwargs["alt"] = ""
                file = file.format(**kwargs)
            self.s.sendall(file.encode('utf-8'))
            data = self.s.recv(1024)
            Logger.getLogger().debug("Data received from js: %s", data)
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
            self.coords["tr"] = int(round(coords["tr"]))
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
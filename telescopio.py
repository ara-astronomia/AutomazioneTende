import socket,json
from base.base_telescopio import BaseTelescopio
from logger import Logger

class Telescopio(BaseTelescopio):

    def __init__(self,hostname, port, script, script_park):
        self.hostname = hostname
        self.port = port
        self.script = script
        self.script_park = script_park
        self.connected = False

    def open_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.hostname, self.port))
        self.connected = True

    def coords(self):
        Logger.getLogger().info("Leggo le coordinate")
        data = self.__call_thesky__(self.script)
        Logger.getLogger().debug("Coordinate lette")
        return self.__parse_result__(data.decode("utf-8"))

    def park_tele(self):
        Logger.getLogger().info("metto in park il telescopio")
        data = self.__call_thesky__(self.script_park)
        Logger.getLogger().debug("Telescopio inviato alla posizione di park")

    def __call_thesky__(self, script):
        with open(script, 'r') as p:
            file = p.read().encode('utf-8')
            self.s.sendall(file)
            Logger.getLogger().info("file inviato")
            data = self.s.recv(1024)
            Logger.getLogger().info(data)
            return data

    def __parse_result__(self,data):
        error = data.find("No error") == -1 or data.find('undefined') > -1
        Logger.getLogger().debug("Errore Telescopio: "+str(error))
        if error:
            jsonString = '{"error": true}'
            coords = json.loads(jsonString)
        else:
            jsonStringEnd = data.find("|")
            jsonString = data[:jsonStringEnd]
            coords = json.loads(jsonString)
            coords["alt"] = int(coords["alt"])
            coords["az"] = int(coords["az"])
        Logger.getLogger().debug("Coords Telescopio: "+str(coords))
        return coords

    def close_connection(self):
        if self.connected:
#            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.connected = False

if __name__ == '__main__':
    netcat("192.168.1.3", 3030, 'MountGetAltAzi.js', 'SetTelPark.js')

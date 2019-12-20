import socket,json
from base.base_telescopio import BaseTelescopio
from logger import Logger

class Telescopio(BaseTelescopio):

    def __init__(self,hostname, port, script, script_park):
        self.hostname = hostname
        self.port = port
        self.script = script
        self.script_park = script_park

    def coords(self):
        with open(self.script, 'r') as f:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.hostname, self.port))
            s.sendall(f.read().encode('utf-8'))
            data = s.recv(1024)
            s.close()
            return self.__parse_result__(data.decode("utf-8"))

    def park_tele(self):
        Logger.getLogger().info("metodo in telescopio")
        with open(self.script_park, 'r') as p:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.hostname, self.port))
            s.sendall(p.read().encode('utf-8'))
            Logger.getLogger().info("inviato con sendall")
            #data = s.recv(1024)
            s.close()
            #return self.__parse_result__(data.decode("utf-8"))


    def __parse_result__(self,data):
        error = data.find("No error")
        if error > -1:
            jsonStringEnd = data.find("|")
            jsonString = data[:jsonStringEnd]
        else:
            jsonString = '{"error": true}'
        coords = json.loads(jsonString)
        coords["alt"] = int(coords["alt"])
        coords["az"] = int(coords["az"])
        return coords

if __name__ == '__main__':
    netcat("192.168.1.22", 3030, 'MountGetAltAzi.js', 'SetparkTel.js')

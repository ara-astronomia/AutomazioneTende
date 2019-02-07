import socket,json
from base_telescopio import BaseTelescopio

class Telescopio(BaseTelescopio):

    def __init__(self,hostname, port, script):
        self.hostname = hostname
        self.port = port
        self.script = script

    def coords(self):
        with open(self.script, 'r') as f:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.hostname, self.port))
            s.sendall(f.read().encode('utf-8'))
            data = s.recv(1024)
            s.close()
            return self.__parse_result__(data.decode("utf-8"))

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
    netcat("192.168.0.9", 3040, 'MountGetAltAzi.js')
import socket,json

def netcat(hostname, port, f):
    return {'alt': "1", 'az': "0"}

if __name__ == '__main__':
    netcat("192.168.0.9", 3040, 'MountGetAltAzi.js')

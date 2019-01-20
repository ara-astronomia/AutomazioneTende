import socket,json

def netcat(hostname, port, f):
    with open(f, 'r') as f:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendall(f.read().encode('utf-8'))
        data = s.recv(1024)
        s.close()
        return parse_result(data.decode("utf-8"))

def parse_result(data):
    error = data.find("No error")
    if error > -1:
        jsonStringEnd = data.find("|")
        jsonString = data[:jsonStringEnd]
    else:
        jsonString = '{"error": true}'
    return json.loads(jsonString)

if __name__ == '__main__':
    netcat("192.168.0.9", 3040, 'MountGetAltAzi.js')

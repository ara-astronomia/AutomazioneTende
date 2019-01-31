import socket,json

def netcat(hostname, port, f):
    alt = input("Inserisci l'altezza del telescopio: ")
    az = input("Inserisci l'azimut del telescopio: ")
    if not is_number(alt) or int(alt) < 0 or int(alt) > 90:
        print("Inserire un numero compreso tra 0 e 90 per l'altezza")
        return netcat(hostname, port, f)
    if not is_number(az) or int(az) < 0 or int(az) > 360:
        print("Inserire un numero compreso tra 0 e 360 per l'azimut")
        return netcat(hostname, port, f)
    return {'alt': int(alt), 'az': int(az)}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

if __name__ == '__main__':
    netcat("192.168.0.9", 3040, 'MountGetAltAzi.js')

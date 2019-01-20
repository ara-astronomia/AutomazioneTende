import time, read_altaz_mount_coord_from_theskyx, config

def read_altaz_mount_coordinate():

    """Leggi le coordinate della montatura"""
    if config.Config.getValue("test") is "1":
        coord = { 'alt': "1", 'az': "0"}
    else:
        coord = read_altaz_mount_coord_from_theskyx.netcat("192.168.0.9", 3040, 'MountGetAltAzi.js')
    print(coord['alt'])
    print(coord['az'])
    return coord

def read_curtains_height():

    """Leggi l'altezza delle tende"""

    pass

def move_curtains_height(coord):

    """Muovi l'altezza delle tende"""

    pass

def park_curtains():

    """Metti a zero l'altezza delle tende"""

    pass

def diff_coordinates(prevCoord, coord):

    """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

    pass

while True:
    prevCoord = park_curtains()
    coord = read_altaz_mount_coordinate()
    if diff_coordinates(prevCoord, coord):
        move_curtains_height(coord)
    time.sleep(int(config.Config.getValue("sleep")))

import time, read_altaz_mount_coord_from_theskyx, config

def read_altaz_mount_coordinate():

    """Leggi le coordinate della montatura"""
    if config.Config.getValue("test") is "1":
        coord = { 'alt': "1", 'az': "0"}
    else:
        try:
            coord = read_altaz_mount_coord_from_theskyx.netcat(config.Config.getValue("theskyx_server"), 3040, config.Config.getValue('altaz_mount_file'))
        except ConnectionRefusedError:
            print("Server non raggiungibile, se si è in test, portare la relativa chiave a 1")
            exit(-1)

    print(coord['alt'])
    print(coord['az'])
    return coord

def read_curtains_height():

    """Leggi l'altezza delle tende"""

    pass

def move_curtains_height(coord):

    """Muovi l'altezza delle tende"""

    # TODO verifica altezza del tele:
    # if inferiore a est_min_height e ovest_min_height
    #   muovi entrambe le tendine a 0
    # else if superiore a est_max_height e ovest_max_height
    #   entrambe le tendine completamente alzate
    # else if superiore a est_min_height e azimut del tele a ovest
    #   alza completamente la tendina est
    #   if inferiore a ovest_min_height
    #     muovi la tendina ovest a 0
    #   else
    #     muovi la tendina ovest a f(altezza telescopio - x)
    # else if superiore a ovest_min_height e azimut del tele a est
    #   alza completamente la tendina est
    #   if inferiore a est_min_height
    #     muovi la tendina est a 0
    #   else
    #     muovi la tendina est a f(altezza telescopio - x)

    pass

def park_curtains():

    """Metti a zero l'altezza delle tende"""
    # TODO muovi i motori portando a zero le tendine
    return { 'alt': "0", 'az': None}

def diff_coordinates(prevCoord, coord):

    """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

    pass

coord = park_curtains()
while True:
    prevCoord = coord
    coord = read_altaz_mount_coordinate()
    if diff_coordinates(prevCoord, coord):
        move_curtains_height(coord)
    time.sleep(int(config.Config.getValue("sleep")))

import time, read_altaz_mount_coord_from_theskyx, config, motorControl ,encoder


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
7.71
    """Muovi l'altezza delle tende"""

    # TODO verifica altezza del tele:
    # if inferiore a est_min_height e ovest_min_height
    #   muovi entrambe le tendine a 0
        go_in_closed_motor_e.motor_control()
        if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()
        
        go_in_closed_motor_w.motor_control()
        if encoder_west.encoder(condition_w) == 'Stop':
            stop_motor_w.motor_control()    
            
              
    # else if superiore a est_max_height e ovest_max_height
    #   entrambe le tendine completamente alzate
        go_in_open_motor_e.motor_control()
        if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()
        
        go_in_open_motor_w.motor_control()
        if encoder_west.encoder(condition_w) == 'Stop':
            stop_motor_w.motor_control() 
                
                
    # else if superiore a est_min_height e azimut del tele a ovest
    # else if azimut compreso tra azSE e azNE: (qui bisognerà fare dei conti differenziali perchè passiamo lo 0 dell'azimut e giriamo in senso oriario) 
    #   alza completamente la tendina est
        go_in_open_motor_e.motor_control()
        if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()  
    #   if inferiore a ovest_min_height
    #     muovi la tendina ovest a 0
        go_in_closed_motor_w.motor_control()
        if encoder_west.encoder(condition_w) == 'Stop':
            stop_motor_w.motor_control()
    #   else
    #     muovi la tendina ovest a f(altezza telescopio - x)
    # else if superiore a ovest_min_height e azimut del tele a est
    #   alza completamente la tendina est
        go_in_open_motor_e.motor_control()
        if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()
    #   if inferiore a est_min_height
    #     muovi la tendina est a 0
        go_in_closed_motor_e.motor_control()
        if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()    
    #   else
    #     muovi la tendina est a f(altezza telescopio - x)

    pass

def park_curtains():

    """Metti a zero l'altezza delle tende"""
    # TODO muovi i motori portando a zero le tendine
    go_in_open_motor_e.motor_control()
    if encoder_est.encoder(condition_e) == 'Stop':
            stop_motor_e.motor_control()
    
    go_in_open_motor_w.motor_control()
    if encoder_west.encoder(condition_w) == 'Stop':
            stop_motor_w.motor_control()     
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

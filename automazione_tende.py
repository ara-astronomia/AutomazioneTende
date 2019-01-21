import time, config
if config.Config.getValue("test") is "1":
    import mock.read_altaz_mount_coord_from_theskyx as read_altaz_mount_coord_from_theskyx
    import mock.motor_control as motor_control
    import mock.encoder as encoder
else:
    import read_altaz_mount_coord_from_theskyx, motor_control, encoder


def read_altaz_mount_coordinate():

    """Leggi le coordinate della montatura"""
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

    condition_e = None # da calcolare
    condition_w = None # da calcolare
    # TODO verifica altezza del tele:
    # if inferiore a est_min_height e ovest_min_height
    #   muovi entrambe le tendine a 0
    motor_control.go_in_closed_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
        motor_control.stop_motor_e()

    motor_control.go_in_closed_motor_w()
    if encoder.encoder_west(condition_w) == 'Stop':
        motor_control.stop_motor_w()

    # else if superiore a est_max_height e ovest_max_height
    #   entrambe le tendine completamente alzate
    motor_control.go_in_open_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
        motor_control.stop_motor_e()

    motor_control.go_in_open_motor_w()
    if encoder.encoder_west(condition_w) == 'Stop':
        motor_control.stop_motor_w()

    # else if superiore a est_min_height e azimut del tele a ovest
    # else if azimut compreso tra azSE e azNE: (qui bisognerà fare dei conti differenziali perchè passiamo lo 0 dell'azimut e giriamo in senso oriario)
    #   alza completamente la tendina est
    motor_control.go_in_open_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
        motor_control.stop_motor_e()

    #   if inferiore a ovest_min_height
    #     muovi la tendina ovest a 0
    motor_control.go_in_closed_motor_w()
    if encoder.encoder_west(condition_w) == 'Stop':
        motor_control.stop_motor_w()

    #   else
    #     muovi la tendina ovest a f(altezza telescopio - x)
    # else if superiore a ovest_min_height e azimut del tele a est
    #   alza completamente la tendina est
    motor_control.go_in_open_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
        motor_control.stop_motor_e()
    #   if inferiore a est_min_height
    #     muovi la tendina est a 0

    motor_control.go_in_closed_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
        motor_control.stop_motor_e()
    #   else
    #     muovi la tendina est a f(altezza telescopio - x)

    pass

def park_curtains():

    """Metti a zero l'altezza delle tende"""

    condition_e = None # da calcolare
    condition_w = None # da calcolare

    # TODO muovi i motori portando a zero le tendine
    motor_control.go_in_open_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
            motor_control.stop_motor_e()

    motor_control.go_in_open_motor_w()
    if encoder.encoder_west(condition_w) == 'Stop':
            motor_control.stop_motor_w()
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

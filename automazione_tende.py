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

def move_curtains_height(prevCoord,coord):

    """Muovi l'altezza delle tende"""
    alt_max_tend_e = config.Config.getValue("tenda_max_est")
    alt_max_tend_w = config.Config.getValue("tenda_max_west")
    alt_min_tel_e = config.Config.getValue("alt_min_tel_e")
    alt_min_tel_w = config.Config.getValue("alt_min_tel_w")

    # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
    increm_e = (config.Config.getValue("tenda_max_est")-config.Config.getValue("tenda_park_est"))/config.Config.getValue('n_step_corsa_tot')
    increm_w = (config.Config.getValue("tenda_max_west")-config.Config.getValue("tenda_park_west"))/config.Config.getValue('n_step_corsa_tot')

    condition_e = None # da calcolare
    condition_w = None # da calcolare
    # TODO verifica altezza del tele:

    # telescopio sopra tenda Est
    # alza completamente tenda West
    if azSE > (coord['az']) > azNE:
        # controllo h_tenda_W = max
        motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
        if encoder.encoder_west(condition_w) == 'Stop': # controllo condizione encoder
            motor_control.stop_motor_w() # chiamo il comando per lo stop del motore

        # controllo h_tenda_E = (coord['alt']) - x # x = parametro di sicurezza
        if prevCoord['alt'] > coord['alt']:
            if coord['alt'] <= alt_min_tel_e: #y altezza minima puntamento telescopio
                # h_tenda_E = 0
                motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso chiusura
                if encoder.encoder_est(condition_e) == 'Stop': # controllo condizione encoder
                    motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            else:
                delta_coord= prevCoord['alt']-coord['alt'] # calcolo la differenza del valore di altezza tra le ultime due posizioni del tele
                move_for_step = delta_coord/increm_e # calcolo gli step corrispondenti al delta_coord
                last_encoder_est_condition = encoder.encoder_est(condition) # leggo l'ultima posizione dell'encoder
                motor_control.go_in_closed_motor_e() # chiamo la funzione di start del motore verso chiusura
                if encoder.encoder_est(condition) <= last_encoder_est_condition - move_for_step: # comparo la lettura dell'encoder con il valore raggiungere
                    motor_control.stop_motor_e()  # chiamo il comando per lo stop del motore


        else:
            #controllo altezza minima puntamento telescopio
            if coord['alt'] <= alt_min_tel_e: #y altezza minima puntamento telescopio
                # h_tenda_E = 0
                motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso chiusura
                if encoder.encoder_est(condition_e) == 'Stop': # controllo condizione encoder
                    motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            else:
                delta_coord= coord['alt']-prevCoord['alt'] # calcolo la differenza del valore di altezza tra le ultime due posizioni del tele
                move_for_step = delta_coord/increm_e # calcolo gli step corrispondenti al delta_coord
                last_encoder_est_condition = encoder.encoder_est(condition) # leggo l'ultima posizione dell'encoder
                motor_control.go_in_open_motor_e() # chiamo la funzione di start del motore verso apertura
                if encoder.encoder_est(condition) >= last_encoder_est_condition + move_for_step: # comparo la lettura dell'encoder con il valore da raggiungere
                    motor_control.stop_motor_e()  # chiamo il comando per lo stop del motore



    # telescopio sopra tenda West
    # alza completamente la tendina est
    if azNW > (coord['az']) > azSW:
        # controllo h_tenda_E = max
        motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
        if encoder.encoder_est(condition_e) == 'Stop': # controllo condizione encoder
            motor_control.stop_motor_e() # chiamo il comando per lo stop del motore

        # controllo h_tenda_W = (coord['alt']) - x # x = parametro di sicurezza
        if prevCoord['alt'] > coord['alt']:
            if coord['alt'] <= alt_min_tel_w: #y altezza minima puntamento telescopio
                # h_tenda_W = 0
                motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso chiusura
                if encoder.encoder_est(condition_w) == 'Stop': # controllo condizione encoder
                    motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            else:
                delta_coord= prevCoord['alt']-coord['alt'] # calcolo la differenza del valore di altezza tra le ultime due posizioni del tele
                move_for_step = delta_coord/increm_w # calcolo gli step corrispondenti al delta_coord
                last_encoder_west_condition = encoder.encoder_west(condition) # leggo l'ultima posizione dell'encoder
                motor_control.go_in_closed_motor_w() # chiamo la funzione di start del motore verso chiusura
                if encoder.encoder_west(condition) <= last_encoder_west_condition - move_for_step: # comparo la lettura dell'encoder con il valore raggiungere
                    motor_control.stop_motor_w()  # chiamo il comando per lo stop del motore


        else:
            #controllo altezza minima puntamento telescopio
            if coord['alt'] <= alt_min_tel_w: #y altezza minima puntamento telescopio
                # h_tenda_W = 0
                motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso chiusura
                if encoder.encoder_west(condition_w) == 'Stop': # controllo condizione encoder
                    motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            else:
                delta_coord= coord['alt']-prevCoord['alt'] # calcolo la differenza del valore di altezza tra le ultime due posizioni del tele
                move_for_step = delta_coord/increm_w # calcolo gli step corrispondenti al delta_coord
                last_encoder_west_condition = encoder.encoder_west(condition) # leggo l'ultima posizione dell'encoder
                motor_control.go_in_open_motor_w() # chiamo la funzione di start del motore verso apertura
                if encoder.encoder_west(condition) >= last_encoder_west_condition + move_for_step: # comparo la lettura dell'encoder con il valore da raggiungere
                    motor_control.stop_motor_w()  # chiamo il comando per lo stop del motore


    # if inferiore a est_min_height e ovest_min_height
    # muovi entrambe le tendine a 0
    if (coord['alt']) <= az_park_tend_e and (coord['alt']) <= alt_park_tend_w: #az_park_tend e alt_park_tend valori di az e alt tende in posizione chiusura
        # h_tenda_E = 0
        motor_control.go_in_closed_motor_e()
        if encoder.encoder_est(condition_e) == 'Stop':
            motor_control.stop_motor_e()
        # h_tenda_W = 0
        motor_control.go_in_closed_motor_w()
        if encoder.encoder_west(condition_w) == 'Stop':
            motor_control.stop_motor_w()

    # else if superiore a est_max_height e ovest_max_height
    # entrambe le tendine completamente alzate
    if azNE > (coord['alt']) > 0 or azSW > (coord['alt']) > azSE or 360 > (coord['alt']) > azNW or ((coord['alt']) > alt_max_tend_e and (coord['alt']) > alt_max_tend_w):
        # h_tenda_E = max
        motor_control.go_in_open_motor_e()
        if encoder.encoder_est(condition_e) == 'Stop':
            motor_control.stop_motor_e()
        # h_tenda_W = max
        motor_control.go_in_open_motor_w()
        if encoder.encoder_west(condition_w) == 'Stop':
            motor_control.stop_motor_w()

def park_curtains():

    """Metti a zero l'altezza delle tende"""

    condition_e = None # da calcolare
    condition_w = None # da calcolare

    # TODO muovi i motori portando a zero le tendine
    motor_control.go_in_closed_motor_e()
    if encoder.encoder_est(condition_e) == 'Stop':
            motor_control.stop_motor_e()

    motor_control.go_in_closed_motor_w()
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
        move_curtains_height(pervCoord, coord)
    time.sleep(int(config.Config.getValue("sleep")))

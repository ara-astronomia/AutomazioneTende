import PySimpleGUI as sg  
import time, config
if config.Config.getValue("test") is "1":
    import mock.read_altaz_mount_coord_from_theskyx as read_altaz_mount_coord_from_theskyx
    import mock.motor_control as motor_control
    import mock.encoder as encoder
else:
    import read_altaz_mount_coord_from_theskyx, motor_control, encoder
p=''
direction=''
prog_e = encoder.Encoder.__save_current_step__(p,direction)

alt_max_tend_e = int(config.Config.getValue("max_est", "tende"))
alt_max_tend_w = int(config.Config.getValue("max_west", "tende"))
alt_min_tend_e = int(config.Config.getValue("park_est", "tende"))
alt_min_tend_w = int(config.Config.getValue("park_west", "tende"))
alt_min_tel_e = config.Config.getValue("alt_min_tel_e")
alt_min_tel_w = config.Config.getValue("alt_min_tel_w")
n_step_corsa_tot = int(config.Config.getValue('n_step_corsa_tot', "encoder_step"))

azimut_ne = int(config.Config.getValue("azNE", "azimut"))
azimut_se = int(config.Config.getValue("azSE", "azimut"))
azimut_sw = int(config.Config.getValue("azSW", "azimut"))
azimut_nw = int(config.Config.getValue("azNW", "azimut"))

# stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
increm_e = (alt_max_tend_e-alt_min_tend_e)/n_step_corsa_tot
increm_w = (alt_max_tend_w-alt_min_tend_w)/n_step_corsa_tot


encoder_est = encoder.Encoder("E")
encoder_west = encoder.Encoder("W")

sg.ChangeLookAndFeel('GreenTan')  
# Design pattern 1 - First window does not remain active  

menu_def = [['File', ['Exit']],      
            ['Help', 'About...']] 
layout = [[sg.Menu(menu_def, tearoff=True)],
         [sg.Text('Controllo movimento tende ', size=(30, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],             
         [sg.Text('altezza telescopio')],
         [sg.ProgressBar((n_step_corsa_tot), orientation='h', size=(20, 20), key='progbar_e')],
         [sg.ProgressBar((n_step_corsa_tot), orientation='h', size=(20, 20), key='progbar_w')],
         [sg.Button('StartTende')],[sg.Button('Exit')]]  

win1 = sg.Window('Controllo tende Osservatorio').Layout(layout)  
while True:  
    ev1, vals1 = win1.Read()
    print ("corsa in step: "+str(n_step_corsa_tot))
    print ("gradi escursione tende: "+ str(alt_max_tend_e-alt_min_tend_e))
    print ("gradi per step: "+ "{0:.3f}".format(increm_e))
    print ("primi per step: "+ "{0:.3f}".format(increm_e*60))

    def read_altaz_mount_coordinate():

        """Leggi le coordinate della montatura"""
        try:
            coord = read_altaz_mount_coord_from_theskyx.netcat(config.Config.getValue("theskyx_server"), 3040, config.Config.getValue('altaz_mount_file'))
        except ConnectionRefusedError:
            print("Server non raggiungibile, se si è in test, portare la relativa chiave a 1")
            exit(-1)

        print("Altezza Telescopio: "+str(coord['alt']))
        print("Azimut Telescopio: "+str(coord['az']))
        return coord

    def read_curtains_height():

        """Leggi l'altezza delle tende"""

        pass

    def move_curtains_height(coord):
        
        #e= prog_e()
       
        """Muovi l'altezza delle tende"""

        # TODO verifica altezza del tele:
        # if inferiore a est_min_height e ovest_min_height
        if coord["alt"] <= alt_min_tend_e and coord["alt"] <= alt_min_tend_w:
            #   muovi entrambe le tendine a 0
            park_curtains()
            # else if superiore a est_max_height e ovest_max_height
        elif coord["alt"] >= alt_max_tend_e and coord["alt"] >= alt_max_tend_w:
            #   entrambe le tendine completamente alzate
            motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
            encoder_west.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_w() # chiamo il comando per lo stop del motore

            motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
            encoder_est.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            # else if superiore a est_min_height e azimut del tele a ovest
        elif azimut_sw < coord["az"] <= azimut_nw:
            #   alza completamente la tendina est
            motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
            encoder_est.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            #   if inferiore a ovest_min_height
            if coord["alt"] <= alt_min_tend_w:
                #     muovi la tendina ovest a 0
                motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso apertura
                encoder_west.listen_until(0) # controllo condizione encoder
                motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina ovest a f(altezza telescopio - x)
                step_w = (coord["alt"]-alt_min_tend_w)/increm_w
                if encoder_west.current_step > step_w:
                    motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso apertura
                else:
                    motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
                encoder_west.listen_until(step_w) # controllo condizione encoder
                motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            # else if superiore a ovest_min_height e azimut del tele a est
        elif azimut_ne <= coord["az"] <= azimut_se:
            #   alza completamente la tendina ovest
            motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
            encoder_west.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            #   if inferiore a est_min_height
            if coord["alt"] <= alt_min_tend_e:
                #     muovi la tendina est a 0
                motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso apertura
                encoder_est.listen_until(0) # controllo condizione encoder
                motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina est a f(altezza telescopio - x)
                step_e = (coord["alt"]-alt_min_tend_e)/increm_e
                if encoder_est.current_step > step_e:
                    motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso apertura
                else:
                    motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
                encoder_est.listen_until(step_e) # controllo condizione encoder
                motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
        
        elif azimut_ne > (coord['az']) > 0 or azimut_sw > (coord['az']) > azimut_se or 360 > (coord['az']) > azimut_nw or ((coord['alt']) > alt_max_tend_e and (coord['alt']) > alt_max_tend_w):
            motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
            encoder_west.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            
            motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
            encoder_est.listen_until(n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
    
        print (str(prog_e) +'progressivo')
        #win1.FindElement('progbar_e').UpdateBar(coord['alt'])
        #print(encoder_west.listen_until(current_step))
        win1.FindElement('progbar_e').UpdateBar(coord['alt'])
        #win1.FindElement('progbar_w').UpdateBar(west)            
    

    def park_curtains():

        """Metti a zero l'altezza delle tende"""

        motor_control.go_in_closed_motor_e()
        encoder_est.listen_until(0)
        motor_control.stop_motor_e()

        motor_control.go_in_closed_motor_w()
        encoder_west.listen_until(0)
        motor_control.stop_motor_w()

        return { 'alt': 0, 'az': 0}

    def diff_coordinates(prevCoord, coord):

        """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

        return abs(coord["alt"] - prevCoord["alt"]) > 5 or abs(coord["az"] - prevCoord["az"]) > 5
    
    
    
    try:
        coord = park_curtains()
        prevCoord = coord
        while True:
            coord = read_altaz_mount_coordinate()
            if diff_coordinates(prevCoord, coord):
                move_curtains_height(coord)
                # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
                # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
                prevCoord = coord
            time.sleep(config.Config.getFloat("sleep"))
    




    except KeyboardInterrupt:
        print("")
        print("Uscita dall'applicazione")
        exit(0)

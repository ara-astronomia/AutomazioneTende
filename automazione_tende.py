import PySimpleGUI as sg
import time, config
if config.Config.getValue("test") is "1":
    import mock.read_altaz_mount_coord_from_theskyx as read_altaz_mount_coord_from_theskyx
    import mock.motor_control as motor_control
    import mock.encoder as encoder
else:
    import read_altaz_mount_coord_from_theskyx, motor_control, encoder

class AutomazioneTende:
    def __init__(self):
        self.alt_max_tend_e = int(config.Config.getValue("max_est", "tende"))
        self.alt_max_tend_w = int(config.Config.getValue("max_west", "tende"))
        self.alt_min_tend_e = int(config.Config.getValue("park_est", "tende"))
        self.alt_min_tend_w = int(config.Config.getValue("park_west", "tende"))
        self.alt_min_tel_e = config.Config.getValue("alt_min_tel_e")
        self.alt_min_tel_w = config.Config.getValue("alt_min_tel_w")
        self.n_step_corsa_tot = int(config.Config.getValue('n_step_corsa_tot', "encoder_step"))

        self.azimut_ne = int(config.Config.getValue("azNE", "azimut"))
        self.azimut_se = int(config.Config.getValue("azSE", "azimut"))
        self.azimut_sw = int(config.Config.getValue("azSW", "azimut"))
        self.azimut_nw = int(config.Config.getValue("azNW", "azimut"))

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa_tot
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa_tot

        self.encoder_est = encoder.Encoder("E")
        self.encoder_west = encoder.Encoder("W")

        self.theskyx_server = config.Config.getValue("theskyx_server")
        self.altaz_mount_file = config.Config.getValue('altaz_mount_file')

    def read_altaz_mount_coordinate(self):

        """Leggi le coordinate della montatura"""
        try:
            coord = read_altaz_mount_coord_from_theskyx.netcat(self.theskyx_server, 3040, self.altaz_mount_file)
        except ConnectionRefusedError:
            print("Server non raggiungibile, se si è in test, portare la relativa chiave a 1")
            exit(-1)

        print("Altezza Telescopio: "+str(coord['alt']))
        print("Azimut Telescopio: "+str(coord['az']))
        return coord

    def read_curtains_height(self):

        """Leggi l'altezza delle tende"""

        pass

    def move_curtains_height(self, coord):

        #e= prog_e()

        """Muovi l'altezza delle tende"""

        # TODO verifica altezza del tele:
        # if inferiore a est_min_height e ovest_min_height
        if coord["alt"] <= self.alt_min_tend_e and coord["alt"] <= self.alt_min_tend_w:
            #   muovi entrambe le tendine a 0
            self.park_curtains()
            # else if superiore a est_max_height e ovest_max_height
        elif coord["alt"] >= self.alt_max_tend_e and coord["alt"] >= self.alt_max_tend_w:
            #   entrambe le tendine completamente alzate
            self.open_all_curtains()
            # else if superiore a est_min_height e azimut del tele a ovest
        elif self.azimut_ne > (coord['az']) > 0 or self.azimut_sw > (coord['az']) > self.azimut_se or 360 > (coord['az']) > self.azimut_nw or ((coord['alt']) > self.alt_max_tend_e and (coord['alt']) > self.alt_max_tend_w):
            self.open_all_curtains()
        elif self.azimut_sw < coord["az"] <= self.azimut_nw:
            #   alza completamente la tendina est
            motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
            self.encoder_est.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            #   if inferiore a ovest_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #     muovi la tendina ovest a 0
                motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso apertura
                self.encoder_west.listen_until(0) # controllo condizione encoder
                motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina ovest a f(altezza telescopio - x)
                step_w = (coord["alt"]-self.alt_min_tend_w)/self.increm_w
                if self.encoder_west.current_step > step_w:
                    motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso apertura
                else:
                    motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
                self.encoder_west.listen_until(step_w) # controllo condizione encoder
                motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            # else if superiore a ovest_min_height e azimut del tele a est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   alza completamente la tendina ovest
            motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
            self.encoder_west.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
            motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            #   if inferiore a est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                #     muovi la tendina est a 0
                motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso apertura
                self.encoder_est.listen_until(0) # controllo condizione encoder
                motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina est a f(altezza telescopio - x)
                step_e = (coord["alt"]-self.alt_min_tend_e)/self.increm_e
                if self.encoder_est.current_step > step_e:
                    motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso apertura
                else:
                    motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
                self.encoder_est.listen_until(step_e) # controllo condizione encoder
                motor_control.stop_motor_e() # chiamo il comando per lo stop del motore

    def park_curtains(self):

        """Metti a zero l'altezza delle tende"""

        motor_control.go_in_closed_motor_e()
        self.encoder_est.listen_until(0)
        motor_control.stop_motor_e()

        motor_control.go_in_closed_motor_w()
        self.encoder_west.listen_until(0)
        motor_control.stop_motor_w()

        return { 'alt': 0, 'az': 0}

    def open_all_curtains(self):
        motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
        self.encoder_west.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
        motor_control.stop_motor_w() # chiamo il comando per lo stop del motore

        motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
        self.encoder_est.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
        motor_control.stop_motor_e() # chiamo il comando per lo stop del motore

    def diff_coordinates(self, prevCoord, coord):

        """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

        return abs(coord["alt"] - prevCoord["alt"]) > 5 or abs(coord["az"] - prevCoord["az"]) > 5

    def console_gui(self):
        try:
            coord = self.park_curtains()
            prevCoord = coord
            while True:
                coord = self.read_altaz_mount_coordinate()
                if self.diff_coordinates(prevCoord, coord):
                    self.move_curtains_height(coord)
                    # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
                    # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
                    prevCoord = coord
                time.sleep(config.Config.getFloat("sleep"))
        except KeyboardInterrupt:
            print("")
            print("Uscita dall'applicazione")
            exit(0)

if __name__ == '__main__':
    automazioneTende = AutomazioneTende()
    automazioneTende.console_gui()

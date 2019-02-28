import time, config

class AutomazioneTende:
#(Thread):
    def __init__(self, mock=False, thesky=False):
#        Thread.__init__(self)
        self.mock = mock
        self.thesky = thesky
        if mock:
            import mock.motor_control as motor_control
            import mock.encoder as encoder
            import mock.roof_control as roof_control
        else:
            import motor_control, encoder, roof_control

        if thesky:
            import telescopio
        else:
            import mock.telescopio as telescopio

        self.roof_control = roof_control
        self.motor_control = motor_control
        self.n_step_corsa_tot = config.Config.getInt('n_step_corsa_tot', "encoder_step")

        self.telescopio = telescopio.Telescopio(config.Config.getValue("theskyx_server"), 3040 ,config.Config.getValue('altaz_mount_file'))
        self.encoder_est = encoder.Encoder("E",self.n_step_corsa_tot)
        self.encoder_west = encoder.Encoder("W",self.n_step_corsa_tot)

        self.started = False
        self.roof = False
        self.prevCoord = { 'alt': 0, 'az': 0 }

        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")
        self.alt_min_tel_e = config.Config.getValue("alt_min_tel_e")
        self.alt_min_tel_w = config.Config.getValue("alt_min_tel_w")

        self.azimut_ne = config.Config.getInt("azNE", "azimut")
        self.azimut_se = config.Config.getInt("azSE", "azimut")
        self.azimut_sw = config.Config.getInt("azSW", "azimut")
        self.azimut_nw = config.Config.getInt("azNW", "azimut")

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa_tot
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa_tot


    def read_altaz_mount_coordinate(self):

        """Leggi le coordinate della montatura"""
        try:
            coords = self.telescopio.coords()
        except ConnectionRefusedError:
            print("Server non raggiungibile, per usare il mock delle coordinate telescopio usare il flag -s per avviare il server")
            coords = {"alt": 0, "az": 0}

        print("Altezza Telescopio: "+str(coords['alt']))
        print("Azimut Telescopio: "+str(coords['az']))
        return coords

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
            self.motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
            self.encoder_est.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
            self.motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            #   if inferiore a ovest_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #     muovi la tendina ovest a 0
                self.motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso chiusura
                self.encoder_west.listen_until(0) # controllo condizione encoder
                self.motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina ovest a f(altezza telescopio - x)
                step_w = (coord["alt"]-self.alt_min_tend_w)/self.increm_w
                if self.encoder_west.current_step > step_w:
                    self.motor_control.go_in_closed_motor_w() # chiamo il comando per attivazione motore verso chiusura
                    self.encoder_west.listen_until(step_w) # controllo condizione encoder
                    self.motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
                else:
                    self.motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
                    self.encoder_west.listen_until(step_w) # controllo condizione encoder
                    self.motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            # else if superiore a ovest_min_height e azimut del tele a est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   alza completamente la tendina ovest
            self.motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
            self.encoder_west.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
            self.motor_control.stop_motor_w() # chiamo il comando per lo stop del motore
            #   if inferiore a est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                #     muovi la tendina est a 0
                self.motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso chiusura
                self.encoder_est.listen_until(0) # controllo condizione encoder
                self.motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
            else:
                #     muovi la tendina est a f(altezza telescopio - x)
                step_e = (coord["alt"]-self.alt_min_tend_e)/self.increm_e
                if self.encoder_est.current_step > step_e:
                    self.motor_control.go_in_closed_motor_e() # chiamo il comando per attivazione motore verso chiusura
                    self.encoder_est.listen_until(step_e) # controllo condizione encoder
                    self.motor_control.stop_motor_e() # chiamo il comando per lo stop del motore
                else:
                    self.motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
                    self.encoder_est.listen_until(step_e) # controllo condizione encoder
                    self.motor_control.stop_motor_e() # chiamo il comando per lo stop del motore

    def park_curtains(self):

        """Metti a zero l'altezza delle tende"""

        self.motor_control.go_in_closed_motor_e()
        self.encoder_est.listen_until(0)
        self.motor_control.stop_motor_e()

        self.motor_control.go_in_closed_motor_w()
        self.encoder_west.listen_until(0)
        self.motor_control.stop_motor_w()

        return { 'alt': 0, 'az': 0 }

    def open_all_curtains(self):
        self.motor_control.go_in_open_motor_w() # chiamo il comando per attivazione motore verso apertura
        self.encoder_west.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
        self.motor_control.stop_motor_w() # chiamo il comando per lo stop del motore

        self.motor_control.go_in_open_motor_e() # chiamo il comando per attivazione motore verso apertura
        self.encoder_est.listen_until(self.n_step_corsa_tot) # controllo condizione encoder
        self.motor_control.stop_motor_e() # chiamo il comando per lo stop del motore

    def diff_coordinates(self, prevCoord, coord):

        """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_azi")

    def open_roof(self):
        status_roof=self.roof_control.verify_closed_roof()
        if status_roof == 1:
            self.roof = True
            return self.roof_control.open_roof()
        return -1

    def close_roof(self):
        status_roof=self.roof_control.verify_open_roof()
        if status_roof == 0 and not self.started:
            self.roof = False
            return self.roof_control.closed_roof()
        return -1

    def exit_program(self,n=0):
        print("")
        print("Uscita dall'applicazione")
        if not self.mock:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        exit(n)

    def run(self):
        self.started = True
        self.coord = self.park_curtains()
        self.prevCoord = self.coord
        while True:
            if not self.exec():
                break

    def exec(self):
        if not self.started:
            self.coord = self.park_curtains()
            self.prevCoord = self.coord
            return 0
        if not self.roof:
            return -1
        self.coord = self.read_altaz_mount_coordinate()
        print(self.coord)
        if self.diff_coordinates(self.prevCoord, self.coord):
            self.prevCoord = self.coord
            self.move_curtains_height(self.coord)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
#        time.sleep(config.Config.getFloat("sleep"))
        return 1

    def console_ui(self):
        try:
            self.exec()
        except KeyboardInterrupt:
          print("Intercettato CTRL+C")
        except Exception as e:
          print("altro errore: "+str(e))
        finally:
          self.exit_program()


if __name__ == '__main__':
    automazioneTende = AutomazioneTende()
    automazioneTende.console_ui()

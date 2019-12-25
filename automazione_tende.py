import time, config
from logger import Logger
from status import Status

class AutomazioneTende:
#(Thread):
    def __init__(self, mock=False, thesky=False):
#        Thread.__init__(self)
        self.mock = mock
        self.thesky = thesky
        if mock:
            from unittest.mock import patch, MagicMock
            from mock.encoders_control import WestEncoder, EastEncoder
            from mock.roof_control import RoofControl
            MockRPi = MagicMock()
            modules = {
                "RPi": MockRPi,
                "RPi.GPIO": MockRPi.GPIO,
            }
            patcher = patch.dict("sys.modules", modules)
            patcher.start()
        else:
            from encoders_control import WestEncoder, EastEncoder
            from roof_control import RoofControl

        if thesky:
            import telescopio
        else:
            import mock.telescopio as telescopio

        self.roof_control = RoofControl()
        self.n_step_corsa_tot = config.Config.getInt('n_step_corsa_tot', "encoder_step")
        self.telescopio = telescopio.Telescopio(config.Config.getValue("theskyx_server"), 3040 ,config.Config.getValue('altaz_mount_file'),config.Config.getValue('park_tele_file'))
        self.encoder_est = EastEncoder()
        self.encoder_west = WestEncoder()

        self.started = False
        self.roof = False
        self.prevCoord = { 'alt': 0, 'az': 0 }

        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")
        self.alt_min_tel_e = config.Config.getValue("alt_min_tel_e", "alt_min_tel")
        self.alt_min_tel_w = config.Config.getValue("alt_min_tel_w", "alt_min_tel")

        self.azimut_ne = config.Config.getInt("azNE", "azimut")
        self.azimut_se = config.Config.getInt("azSE", "azimut")
        self.azimut_sw = config.Config.getInt("azSW", "azimut")
        self.azimut_nw = config.Config.getInt("azNW", "azimut")

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa_tot
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa_tot

    def park_tele(self):
        """ manda il tele alle coordinate AltAz di parking"""
        try:
            park_tele = self.telescopio.park_tele()
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, non è possibile parcheggiare il telescopio")
        #if (coord['az']) == 0 and (coord['alt']) == 0:
        #    Logger.getLogger().error("posizione di park raggiunta")
        return True

    def read_altaz_mount_coordinate(self):

        """Leggi le coordinate della montatura"""
        try:
            coords = self.telescopio.coords()
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, per usare il mock delle coordinate telescopio NON usare il flag -s per avviare il server")
            coords = {"alt": 0, "az": 0}

        Logger.getLogger().debug("Altezza Telescopio: "+str(coords['alt']))
        Logger.getLogger().debug("Azimut Telescopio: "+str(coords['az']))
        print (str(coords['az']))
        return coords

    def read_curtains_height(self):

        """Leggi l'altezza delle tende"""

        pass

    def move_curtains_height(self, coord):

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
            self.encoder_est.move(self.n_step_corsa_tot) # controllo condizione encoder
            #   if inferiore a ovest_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #     muovi la tendina ovest a 0
                self.encoder_west.move(0) # controllo condizione encoder
            else:
                #     muovi la tendina ovest a f(altezza telescopio - x)
                step_w = (coord["alt"]-self.alt_min_tend_w)/self.increm_w
                self.encoder_west.move(step_w) # controllo condizione encoder
            # else if superiore a ovest_min_height e azimut del tele a est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   alza completamente la tendina ovest
            self.encoder_west.move(self.n_step_corsa_tot) # controllo condizione encoder
            #   if inferiore a est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                # muovi la tendina est a 0
                self.encoder_est.move(0) # controllo condizione encoder
            else:
                #     muovi la tendina est a f(altezza telescopio - x)
                step_e = (coord["alt"]-self.alt_min_tend_e)/self.increm_e
                self.encoder_est.move(step_e) # controllo condizione encoder

    def park_curtains(self):

        """Metti a zero l'altezza delle tende"""

        self.encoder_est.move(0)
        self.encoder_west.move(0)

        return { 'alt': 0, 'az': 0 }

    def open_all_curtains(self):
        self.encoder_west.move(self.n_step_corsa_tot) # controllo condizione encoder
        self.encoder_est.move(self.n_step_corsa_tot) # controllo condizione encoder

    def diff_coordinates(self, prevCoord, coord):

        """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_azi")

    def open_roof(self):
        status_roof = self.roof_control.read()
        Logger.getLogger().info("Lo status è " + str(status_roof))
        self.roof = True
        if status_roof != Status.OPEN:
            return self.roof_control.open()
        else:
            return Status.OPEN

    def close_roof(self):
        status_roof = self.roof_control.read()
        if status_roof == Status.OPEN:
            self.roof = False
            return self.roof_control.close()
        elif status_roof == Status.TRANSIT:
            # capire che succede
            pass
        else:
            # già aperto
            pass

    def exit_program(self,n=0):
        from gpio_config import GPIOConfig
        Logger.getLogger().info("Uscita dall'applicazione")
        GPIOConfig().cleanup(n)

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
        Logger.getLogger().debug(self.coord)
        if self.diff_coordinates(self.prevCoord, self.coord):
            self.prevCoord = self.coord
            Logger.getLogger().debug(self.prevCoord)
            self.move_curtains_height(self.coord)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep"))
        return 1

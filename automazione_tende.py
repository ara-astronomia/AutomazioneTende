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
            #from mock.curtains import WestCurtain, EastCurtain
            MockRPi = MagicMock()
            modules = {
                "RPi": MockRPi,
                "RPi.GPIO": MockRPi.GPIO,
            }
            patcher = patch.dict("sys.modules", modules)
            patcher.start()
        else:
            from roof_control import RoofControl
            from curtains import WestCurtain, EastCurtain

        if thesky:
            import telescopio
        else:
            import mock.telescopio as telescopio

        self.roof_control = RoofControl()
        self.n_step_corsa = config.Config.getInt('n_step_corsa', "encoder_step")
        self.telescopio = telescopio.Telescopio(config.Config.getValue("theskyx_server"), 3040 ,config.Config.getValue('altaz_mount_file'),config.Config.getValue('park_tele_file'))
        self.curtain_east = EastCurtain()
        self.curtain_west = WestCurtain()

        self.started = False
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
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa

    def park_tele(self):
        """ manda il tele alle coordinate AltAz di parking"""
        try:
            self.telescopio.open_connection()
            self.telescopio.park_tele()
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, non è possibile parcheggiare il telescopio")
        #if (coord['az']) == 0 and (coord['alt']) == 0:
        #    Logger.getLogger().error("posizione di park raggiunta")
        return True

    def read_altaz_mount_coordinate(self):

        """Leggi le coordinate della montatura"""
        try:
            coords = self.telescopio.coords()
            Logger.getLogger().debug("Telescopio")
            Logger.getLogger().debug("Telescopio: "+str(coords))
            if "error" in coords:
                Logger.getLogger().debug("Errore Telescopio: "+str(coords['error']))
            else:
                Logger.getLogger().debug("Altezza Telescopio: "+str(coords['alt']))
                Logger.getLogger().debug("Azimut Telescopio: "+str(coords['az']))
            return coords
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, per usare il mock delle coordinate telescopio NON usare il flag -s per avviare il server")
            raise

    def read_curtains_height(self):

        """read high curtains"""

        pass

    def move_curtains_height(self, coord):

        """Move curtains to ..."""

        # TODO verify tele height:
        # if less than east_min_height e ovest_min_height
        if coord["alt"] <= self.alt_min_tend_e and coord["alt"] <= self.alt_min_tend_w:
            #   move both curtains to 0
            self.park_curtains()
            # else if higher to east_max_height e ovest_max_height
        elif coord["alt"] >= self.alt_max_tend_e and coord["alt"] >= self.alt_max_tend_w or self.azimut_ne > coord['az'] or coord['az'] > self.azimut_nw or self.azimut_sw > coord['az'] > self.azimut_se:
            #   move both curtains max open
            self.open_all_curtains()

            # else if higher to ovest_min_height and Az tele to west
        elif self.azimut_sw < coord["az"] <= self.azimut_nw:
            #   move curtain east max open
            self.curtain_east.open_up()
            #   if less than west_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #   move curtain west to 0 (closed)
                self.curtain_west.bring_down()
            else:
                #     move curtain west to f(Alt telescope - x)
                step_w = (coord["alt"]-self.alt_min_tend_w)/self.increm_w
                self.curtain_west.move(step_w) # move curtain west to step

            # else if higher to ovest_min_height and Az tele to est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   move curtian west max open
            self.curtain_west.open_up()
            #   if inferior yo est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                # move curtain east to 0 (closed)
                self.curtain_east.bring_down()
            else:
                #     move curtain east to f(Alt tele - x)
                step_e = (coord["alt"]-self.alt_min_tend_e)/self.increm_e
                self.curtain_east.move(step_e) # move curtain east to step

    def park_curtains(self):
        """"move both curtains to 0"""
        self.curtain_east.bring_down()
        self.curtain_west.bring_down()

        return { 'alt': 0, 'az': 0 }

    def open_all_curtains(self):
        """move both curtains max open"""
        self.curtain_east.open_up()
        self.curtain_west.open_up()

    def diff_coordinates(self, prevCoord, coord):

        """Verifica se la differenza tra coordinate giustifichi lo spostamento dell'altezza delle tendine"""

        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_azi")

    def open_roof(self):
        self.telescopio.open_connection()
        status_roof = self.roof_control.read()
        Logger.getLogger().info("Lo status tetto iniziale: %s ", str(status_roof))
        if status_roof != Status.OPEN:
            self.roof_control.open()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))
        return status_roof == Status.OPEN

    def close_roof(self):
        self.telescopio.close_connection()
        status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto iniziale: %s", str(status_roof))
        if status_roof != Status.CLOSED:
            self.roof_control.close()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))
        return status_roof == Status.CLOSED

    def exit_program(self,n=0):
        from gpio_config import GPIOConfig
        Logger.getLogger().info("Uscita dall'applicazione")
        self.telescopio.close_connection()
        GPIOConfig().cleanup(n)

    def exec(self):
        if not self.started:
            self.coord = self.park_curtains()
            self.prevCoord = self.coord
            return 0
        if self.roof_control.read() != Status.OPEN:
            Logger.getLogger().error("TETTO CHIUSO")
            return -1
        current_coord = self.read_altaz_mount_coordinate()
        if "error" not in current_coord:
            self.coord = current_coord
        Logger.getLogger().debug(self.coord)
        if self.diff_coordinates(self.prevCoord, self.coord):
            self.prevCoord = self.coord
            Logger.getLogger().debug(self.prevCoord)
            self.move_curtains_height(self.coord)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep", "automazione"))
        return 1

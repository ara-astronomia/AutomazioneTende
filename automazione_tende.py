import time, config
from logger import Logger
from status import Status, TelescopeStatus, PanelStatus
from typing import Dict, Any
from crac_status import CracStatus

class AutomazioneTende:
#(Thread):
    def __init__(self, mock: bool = False, thesky: bool = False):
#        Thread.__init__(self)
        self.mock = mock
        self.thesky = thesky
        if not mock:
            from roof_control import RoofControl
            from curtains import WestCurtain, EastCurtain
            from panel_control import PanelControl
        else:
            from unittest.mock import patch, MagicMock
            from mock.roof_control import RoofControl # type: ignore
            from mock.curtains import WestCurtain, EastCurtain # type: ignore
            from mock.panel_control import PanelControl
            MockRPi = MagicMock()
            modules = {
                "RPi": MockRPi,
                "RPi.GPIO": MockRPi.GPIO,
            }
            patcher = patch.dict("sys.modules", modules)
            patcher.start()

        if thesky:
            import telescopio
        else:
            import mock.telescopio as telescopio # type: ignore

        self.roof_control = RoofControl()
        self.n_step_corsa = config.Config.getInt('n_step_corsa', "encoder_step")
        self.telescopio = telescopio.Telescopio(config.Config.getValue("theskyx_server"), config.Config.getValue('altaz_mount_file'), config.Config.getValue('park_tele_file'), config.Config.getValue('flat_tele_file'), config.Config.getValue('tracking_on_tele_file'))
        self.curtain_east = EastCurtain()
        self.curtain_west = WestCurtain()
        self.panel_control = PanelControl()

        self.started = False
        self.prevCoord = { 'alt': 0, 'az': 0, 'error': 0 }

        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")

        self.azimut_ne = config.Config.getInt("azNE", "azimut")
        self.azimut_se = config.Config.getInt("azSE", "azimut")
        self.azimut_sw = config.Config.getInt("azSW", "azimut")
        self.azimut_nw = config.Config.getInt("azNW", "azimut")

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa

        self.crac_status = CracStatus()

    def read(self) -> CracStatus:

        """ Read the status of all CRaC components and update the CracStatus object """

        self.crac_status.roof_status = self.roof_control.read()
        self.crac_status.telescope_status = self.telescopio.status
        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps
        self.crac_status.panel_status = self.panel_control.read()
        self.crac_status.tracking_status = self.telescopio.tracking_status
        print (str(self.crac_status) + "questo è il read si crac Status in automazione_tende")

        return self.crac_status

    def park_tele(self) -> Dict[str, int]:

        """ Park the Telescope """

        self.telescopio.park_tele()
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", self.telescopio.status, self.telescopio.coords["alt"], self.telescopio.coords["az"])

        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = self.telescopio.status

        return self.telescopio.coords

    def flat_tele(self) -> Dict[str, int]:
        """ Park the Telescope """

        self.telescopio.flat_tele()
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", self.telescopio.status, self.telescopio.coords["alt"], self.telescopio.coords["az"])

        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = self.telescopio.status

        return self.telescopio.coords

    def read_altaz_mount_coordinate(self) -> Dict[str, int]:

        """ Read Telescope Coordinates """

        self.telescopio.read()
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", self.telescopio.status, self.telescopio.coords["alt"], self.telescopio.coords["az"])

        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = self.telescopio.status

        return self.telescopio.coords

    def is_curtains_status_danger(self) -> bool:

        """ Read the height of the curtains """

        return self.curtain_east.read() == Status.DANGER or self.curtain_west.read() == Status.DANGER

    def move_curtains_height(self, coord: Dict[str, int]):

        """ Change the height of the curtains to based on the given Coordinates """

        # TODO verify tele height:
        # if less than east_min_height e ovest_min_height
        if coord["alt"] <= self.alt_min_tend_e and coord["alt"] <= self.alt_min_tend_w:
            #   move both curtains to 0
            self.park_curtains()
            #   else if higher to east_max_height e ovest_max_height
        elif coord["alt"] >= self.alt_max_tend_e and coord["alt"] >= self.alt_max_tend_w or self.azimut_ne > coord['az'] or coord['az'] > self.azimut_nw or self.azimut_sw > coord['az'] > self.azimut_se:
            #   move both curtains max open
            self.open_all_curtains()

            #   else if higher to ovest_min_height and Az tele to west
        elif self.azimut_sw < coord["az"] <= self.azimut_nw:
            #   move curtain east max open
            self.curtain_east.open_up()
            #   if less than west_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #   move curtain west to 0 (closed)
                self.curtain_west.bring_down()
            else:
                #   move curtain west to f(Alt telescope - x)
                step_w = (coord["alt"]-self.alt_min_tend_w)/self.increm_w
                self.curtain_west.move(int(step_w)) # move curtain west to step

            #   else if higher to ovest_min_height and Az tele to est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   move curtian west max open
            self.curtain_west.open_up()
            #   if inferior to est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                #   move curtain east to 0 (closed)
                self.curtain_east.bring_down()
            else:
                #   move curtain east to f(Alt tele - x)
                step_e = (coord["alt"]-self.alt_min_tend_e)/self.increm_e
                self.curtain_east.move(int(step_e)) # move curtain east to step

        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

        Logger.getLogger().debug("curtain_east_steps %s", self.curtain_east.steps)
        Logger.getLogger().debug("curtain_west_steps %s", self.curtain_west.steps)

    def park_curtains(self) -> None:

        """" Bring down both curtains """

        self.curtain_east.bring_down()
        self.curtain_west.bring_down()

        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

    def open_all_curtains(self):

        """ Open up both curtains to the max extents """

        self.curtain_east.open_up()
        self.curtain_west.open_up()

    def motor_stop(self):
        """ Disable motor control """
        print ('motori stoppati in automazione')
        self.curtain_east.motor_stop()
        self.curtain_west.motor_stop()


    def diff_coordinates(self, prevCoord: Dict[str, int], coord: Dict[str, int]) -> bool:

        """ Check if delta coord is enough to move the curtains """

        Logger.getLogger().debug("Current coord: %s", coord)
        Logger.getLogger().debug("Previous coord: %s", prevCoord)
        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_az")

    def open_roof(self):

        """ Open the roof and update the roof status in CracStatus object """

        status_roof = self.roof_control.read()
        Logger.getLogger().info("Lo status tetto iniziale: %s ", str(status_roof))
        if status_roof != Status.OPEN:
            self.roof_control.open()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))
        self.crac_status.roof_status = status_roof

    def close_roof(self) -> None:

        """ Close the roof and update the roof status in CracStatus object """

        status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto iniziale: %s", str(status_roof))
        if status_roof != Status.CLOSED:
            self.roof_control.close()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))
        self.crac_status.roof_status = status_roof

    def panel_on(self):
        """ on panel flat and update the panel status in CracStatus object """

        status_panel = self.crac_status.panel_status
        Logger.getLogger().debug("Stato del pannello: %s", str(status_panel))
        if status_panel != PanelStatus.ON:
            self.panel_control.panel_on()
            self.telescopio.tele_tracking_on()

    def panel_off(self):
        """ off panel flat and update the panel status in CracStatus object """

        status_panel = self.crac_status.panel_status
        Logger.getLogger().debug("Stato del pannello: %s", str(status_panel))
        if status_panel != PanelStatus.OFF:
            self.panel_control.panel_off()

    def exit_program(self, n: int = 0) -> None:

        """ Shutdown the server """

        from gpio_config import GPIOConfig
        Logger.getLogger().info("Uscita dall'applicazione")
        self.telescopio.close_connection()
        GPIOConfig().cleanup(n)

    def exec(self) -> None:

        """ Move the curtains and update the telescope coordinates"""

        self.coord = self.read_altaz_mount_coordinate()

        if not self.started:
            return

        if self.diff_coordinates(self.prevCoord, self.coord): # TODO diff between steps instead of coords
            self.prevCoord["alt"] = self.coord["alt"]
            self.prevCoord["az"] = self.coord["az"]
            self.prevCoord["error"] = self.coord["error"]
            Logger.getLogger().debug("Differenza coordinate sufficienti")
            self.move_curtains_height(self.coord)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tende non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep", "automazione"))

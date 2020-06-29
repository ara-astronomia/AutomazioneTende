import time
import config
from logger import Logger
from status import Status, TelescopeStatus, ButtonStatus, CurtainsStatus
from typing import Dict, Any
from crac_status import CracStatus
from gpio_pin import GPIOPin


class AutomazioneTende:

    def __init__(self, mock: bool = False, thesky: bool = False):
        self.mock = mock
        self.thesky = thesky
        if not mock:
            from roof_control import RoofControl
            from curtains import WestCurtain, EastCurtain
            from button_control import ButtonControl

        else:
            from unittest.mock import patch, MagicMock
            from mock.roof_control import RoofControl
            from mock.curtains import WestCurtain, EastCurtain
            from mock.button_control import ButtonControl

        if thesky:
            import theskyx.telescope as telescopio
        else:
            import mock.telescope as telescopio

        self.roof_control = RoofControl()
        self.n_step_corsa = config.Config.getInt('n_step_corsa', "encoder_step")
        self.telescope = telescopio.Telescope()
        self.curtain_east = EastCurtain()
        self.curtain_west = WestCurtain()
        self.panel_control = ButtonControl(GPIOPin.SWITCH_PANEL)
        self.power_control = ButtonControl(GPIOPin.SWITCH_POWER)
        self.light_control = ButtonControl(GPIOPin.SWITCH_LIGHT)
        self.aux_control = ButtonControl(GPIOPin.SWITCH_AUX)

        self.started = False

        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")
        self.prevSteps = {'east': self.alt_min_tend_e, 'west': self.alt_min_tend_w}

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al
        # valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa

        self.crac_status = CracStatus()

    def read(self) -> CracStatus:

        """ Read the status of all CRaC components and update the CracStatus object """

        self.crac_status.roof_status = self.roof_control.read()
        self.crac_status.telescope_status = self.telescope.status
        self.crac_status.telescope_coords = self.telescope.coords
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps
        self.crac_status.panel_status = self.panel_control.read()
        self.crac_status.tracking_status = self.telescope.tracking_status
        self.crac_status.power_status = self.power_control.read()
        self.crac_status.light_status = self.light_control.read()
        self.crac_status.aux_status =self.aux_control.read()

        return self.crac_status

    def move_tele(self, tr, alt, az) -> Dict[str, int]:

        """ Move the Telescope nd Tracking off """

        Logger.getLogger().debug("tr %s, alt: %s, az: %s", tr, alt, az)

        self.telescope.move_tele(tr=tr, alt=alt, az=az)
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", self.telescope.status, self.telescope.coords["alt"], self.telescope.coords["az"])

        self.crac_status.telescope_coords = self.telescope.coords
        self.crac_status.telescope_status = self.telescope.status

        return self.telescope.coords

    def read_altaz_mount_coordinate(self) -> Dict[str, int]:

        """ Read Telescope Coordinates """

        self.telescope.read()
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", self.telescope.status, self.telescope.coords["alt"], self.telescope.coords["az"])

        self.crac_status.telescope_coords = self.telescope.coords
        self.crac_status.telescope_status = self.telescope.status

        return self.telescope.coords

    def is_curtains_status_danger(self) -> bool:

        """ Read the height of the curtains """

        danger = CurtainsStatus.DANGER
        curtain_east = self.curtain_east
        curtain_west = self.curtain_west
        return curtain_east.read() is danger or curtain_west.read() is danger

    def move_curtains_steps(self, steps):

        """
            Change the height of the curtains to based
            on the given Coordinates
        """

        if steps["east"] is self.n_step_corsa:
            self.curtain_east.open_up()
        elif steps["east"] == 0:
            self.curtain_east.bring_down()
        else:
            self.curtain_east.move(steps["east"])

        if steps["west"] is self.n_step_corsa:
            self.curtain_west.open_up()
        elif steps["west"] == 0:
            self.curtain_west.bring_down()
        else:
            self.curtain_west.move(steps["west"])

    def calculate_curtains_steps(self):

        """
            Change the height of the curtains
            to based on the given Coordinates
        """

        telescope = self.telescope
        steps = {}
        Logger.getLogger().debug("Telescope status %s", telescope.status)
        # TODO verify tele height:
        # if less than east_min_height e ovest_min_height
        if telescope.status is TelescopeStatus.LOST or telescope.status is TelescopeStatus.ERROR:
            steps["west"] = self.curtain_west.steps
            steps["east"] = self.curtain_east.steps

        if telescope.is_below_curtains_area(0, 0):
            #   keep both curtains to 0
            steps["west"] = 0
            steps["east"] = 0

            #   else if higher to east_max_height e ovest_max_height
        elif telescope.is_above_curtains_area(self.alt_max_tend_e, self.alt_max_tend_w) or not telescope.is_within_curtains_area():
            #   move both curtains max open
            steps["west"] = self.n_step_corsa
            steps["east"] = self.n_step_corsa

            #   else if higher to ovest_min_height and Az tele to west
        elif telescope.status == TelescopeStatus.WEST:
            Logger.getLogger().debug("inside west status")
            #   move curtain east max open
            steps["east"] = self.n_step_corsa
            #   if less than west_min_height
            if telescope.is_below_curtain(self.alt_min_tend_w):
                #   move curtain west to 0 (closed)
                steps["west"] = 0
            else:
                #   move curtain west to f(Alt telescope - x)
                steps["west"] = round((telescope.coords["alt"]-self.alt_min_tend_w)/self.increm_w)

            #   else if higher to ovest_min_height and Az tele to est
        elif telescope.status == TelescopeStatus.EAST:
            Logger.getLogger().debug("inside east status")
            #   move curtian west max open
            steps["west"] = self.n_step_corsa
            #   if inferior to est_min_height
            if telescope.is_below_curtain(self.alt_min_tend_e):
                #   move curtain east to 0 (closed)
                steps["east"] = 0
            else:
                #   move curtain east to f(Alt tele - x)
                steps["east"] = round((telescope.coords["alt"]-self.alt_min_tend_e)/self.increm_e)

        Logger.getLogger().debug("calculatd curtain steps %s", steps)

        return steps

    def park_curtains(self) -> None:

        """" Bring down both curtains """

        self.curtain_east.bring_down()
        self.curtain_west.bring_down()

        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

    def motor_stop(self):

        """ Disable motor control """

        self.curtain_east.motor_stop()
        self.curtain_west.motor_stop()

    def is_diff_steps(self, cs: Dict[str, int], ps: Dict[str, int]) -> bool:

        minDiffSteps = config.Config.getInt("diff_steps", "encoder_step")
        is_east = abs(cs["east"] - ps["east"]) > minDiffSteps
        is_west = abs(cs["west"] - ps["west"]) > minDiffSteps

        return is_east or is_west

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

    # PANEL FLAT
    def panel_on(self):
        """ on panel flat and update the panel status in CracStatus object """

        self.panel_control.on()
        self.telescope.move_tele(tr=1)

    def panel_off(self):
        """ off panel flat and update the panel status in CracStatus object """

        self.panel_control.off()

    # POWER SWITCH
    def power_on(self):
        """ on power switch and update the power switch status in CracStatus object """

        self.power_control.on()

    def power_off(self):
        """ off power switch and update the power switch status in CracStatus object """

        self.power_control.off()

    # LIGHT DOME
    def light_on(self):
        """ on light dome and update the light status in CracStatus object """

        self.light_control.on()

    def light_off(self):
        """ off light dome and update the light status in CracStatus object """

        self.light_control.off()

    # AUXILIARY
    def aux_on(self):
        """ on auxiliary and update the auxiliary status in CracStatus object """

        self.aux_control.on()

    def aux_off(self):
        """ off auxiliary and update the auxiliary status in CracStatus object """

        self.aux_control.off()

    def exit_program(self, n: int = 0) -> None:

        """ Shutdown the server """

        Logger.getLogger().info("Uscita dall'applicazione")
        self.telescope.close_connection()
        if not self.mock:
            Logger.getLogger().debug("Mock: %s", self.mock)
            from gpio_config import GPIOConfig
            GPIOConfig().cleanup(n)

    def exec(self) -> None:

        """ Move the curtains and update the telescope coordinates"""

        steps = self.calculate_curtains_steps()
        Logger.getLogger().debug("calculated steps %s", steps)
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps
        Logger.getLogger().debug("curtain_east_steps %s", self.curtain_east.steps)
        Logger.getLogger().debug("curtain_west_steps %s", self.curtain_west.steps)
        self.read_altaz_mount_coordinate()

        if not self.started:
            self.curtain_east.is_disabled = True
            self.curtain_west.is_disabled = True
            return

        self.curtain_east.is_disabled = False
        self.curtain_west.is_disabled = False
        prevSteps = {"east": self.curtain_east.steps, "west": self.curtain_west.steps}
        if self.is_diff_steps(steps, prevSteps):
            Logger.getLogger().debug("Differenza steps sufficienti")
            self.move_curtains_steps(steps)
            # solo se la differenza è misurabile imposto le coordinate
            # precedenti uguali a quelle attuali altrimenti muovendosi
            # a piccoli movimenti le tende non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep", "automazione"))

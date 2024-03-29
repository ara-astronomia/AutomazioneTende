import datetime
import importlib
from typing import Dict

from components.button_control import ButtonControl
from components.curtains.factory_curtain import FactoryCurtain
from config import Config
from crac_status import CracStatus
from logger import Logger
from status import Status
from status import TelescopeStatus
from status import ButtonStatus
from status import CurtainsStatus
from status import Orientation


class AutomazioneTende:

    def __init__(self, telescope_plugin: str, mock: bool = False):
        self.mock = mock

        if not mock:
            from components.roof_control import RoofControl

        else:
            from gpiozero import Device
            from gpiozero.pins.mock import MockFactory

            from mock.roof_control import MockRoofControl as RoofControl  # type: ignore

            if Device.pin_factory is not None:
                Device.pin_factory.reset()
            Device.pin_factory = MockFactory()

        telescopio = importlib.import_module(f"components.telescope.{telescope_plugin}.telescope")
        self.telescope = telescopio.Telescope()  # type: ignore
        self.roof_control = RoofControl()
        self.n_step_corsa = Config.getInt('n_step_corsa', "encoder_step")

        # TODO: factory shouldn't be aware of the mock
        self.curtain_east = FactoryCurtain.curtain(orientation=Orientation.EAST, mock=self.mock)
        self.curtain_west = FactoryCurtain.curtain(orientation=Orientation.WEST, mock=self.mock)
        self.panel_control = ButtonControl(Config.getInt("switch_panel", "panel_board"))
        self.power_tele_control = ButtonControl(Config.getInt("switch_power", "panel_board"))
        self.light_control = ButtonControl(Config.getInt("switch_light", "panel_board"))
        self.power_ccd_control = ButtonControl(Config.getInt("switch_aux", "panel_board"))

        self.started = False

        self.alt_max_tend_e = Config.getInt("max_est", "tende")
        self.alt_max_tend_w = Config.getInt("max_west", "tende")
        self.alt_min_tend_e = Config.getInt("park_est", "tende")
        self.alt_min_tend_w = Config.getInt("park_west", "tende")
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
        self.crac_status.curtain_east_steps = self.curtain_east.steps()
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps()
        self.crac_status.panel_status = self.panel_control.read()
        self.crac_status.tracking_status = self.telescope.tracking_status
        self.crac_status.slewing_status = self.telescope.slewing_status
        self.crac_status.sync_status = self.telescope.sync_status
        self.crac_status.power_tele_status = self.power_tele_control.read()
        self.crac_status.light_status = self.light_control.read()
        self.crac_status.power_ccd_status = self.power_ccd_control.read()

        return self.crac_status

    def move_tele(self, tr, alt, az) -> Dict[str, int]:

        """ Move the Telescope and set Tracking on/off """

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
        if not self.curtain_east.motor.is_active:
            if steps["east"] is self.n_step_corsa:
                self.curtain_east.open_up()
            elif steps["east"] == 0:
                self.curtain_east.bring_down()
            else:
                self.curtain_east.move(steps["east"])

        if not self.curtain_west.motor.is_active:
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
            steps["west"] = self.curtain_west.steps()
            steps["east"] = self.curtain_east.steps()

        if telescope.is_below_curtains_area():
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
            #   move curtain west to f(Alt telescope - x)
            steps["west"] = round((telescope.coords["alt"]-self.alt_min_tend_w)/self.increm_w)

            #   else if higher to ovest_min_height and Az tele to est
        elif telescope.status == TelescopeStatus.EAST:
            Logger.getLogger().debug("inside east status")
            #   move curtian west max open
            steps["west"] = self.n_step_corsa
            #   if inferior to est_min_height
            #   move curtain east to f(Alt tele - x)
            steps["east"] = round((telescope.coords["alt"]-self.alt_min_tend_e)/self.increm_e)

        Logger.getLogger().debug("calculatd curtain steps %s", steps)

        return steps

    def park_curtains(self) -> None:

        """" Bring down both curtains """

        self.curtain_east.bring_down()
        self.curtain_west.bring_down()

        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps()
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps()

    def motor_stop(self):

        """ Disable motor control """

        self.curtain_east.motor_stop()
        self.curtain_west.motor_stop()

    def is_diff_steps(self, cs: Dict[str, int], ps: Dict[str, int]) -> bool:

        minDiffSteps = Config.getInt("diff_steps", "encoder_step")
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

    def power_on_tele(self):

        """ turn on the power switch and update its status in CracStatus object """

        self.power_tele_control.on()
        self.telescope.sync_time = datetime.datetime.utcnow()
        Logger.getLogger().debug("UTC time di conversione coord per sincronizzazione telescopio %s:", self.telescope.sync_time)

    def power_off_tele(self):

        """ turn off power switch and update its status in CracStatus object """

        self.telescope.nosync()
        self.power_tele_control.off()

    def power_on_ccd(self):

        """ turn on ccd and update its status in CracStatus object """

        self.power_ccd_control.on()

    def power_off_ccd(self):

        """ turn off ccd and update its status in CracStatus object """

        self.power_ccd_control.off()

    def panel_on(self):

        """ turn on panel flat and update its status in CracStatus object """

        self.panel_control.on()
        self.telescope.move_tele(tr=1)

    def panel_off(self):

        """ turn off panel flat and update its status in CracStatus object """

        self.panel_control.off()

    # SYNC SWITCH
    def time_sync(self):
        if self.power_tele_control.read() is ButtonStatus.OFF:
            self.power_on_tele()
        self.telescope.sync()

    def light_on(self):

        """ turn on light on dome and update its status in CracStatus object """

        self.light_control.on()

    def light_off(self):
        """ turn off light on dome and update its status in CracStatus object """

        self.light_control.off()

    def exit_program(self, n: int = 0) -> None:

        """ Shutdown the server """

        Logger.getLogger().info("Uscita dall'applicazione con codice %s", n)
        self.telescope.close_connection()
        self.curtain_east.bring_down()
        self.curtain_west.bring_down()
        self.curtain_east.curtain_closed.wait_for_active()
        self.curtain_west.curtain_closed.wait_for_active()
        self.roof_control.close()

    def exec(self) -> None:

        """ Move the curtains and update the telescope coordinates"""

        steps = self.calculate_curtains_steps()
        Logger.getLogger().debug("calculated steps %s", steps)
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps()
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps()
        Logger.getLogger().debug("curtain_east_steps %s", self.curtain_east.steps())
        Logger.getLogger().debug("curtain_east_status %s", self.curtain_east.read())
        Logger.getLogger().debug("curtain_west_steps %s", self.curtain_west.steps())
        Logger.getLogger().debug("curtain_west_status %s", self.curtain_west.read())
        self.read_altaz_mount_coordinate()

        if self.telescope.status not in [TelescopeStatus.FLATTER, TelescopeStatus.SECURE]:
            self.panel_off()

        if not self.started:
            self.park_curtains()
            self.curtain_east.is_disabled = True
            self.curtain_west.is_disabled = True
            return

        self.curtain_east.is_disabled = False
        self.curtain_west.is_disabled = False
        prevSteps = {"east": self.curtain_east.steps(), "west": self.curtain_west.steps()}
        if self.is_diff_steps(steps, prevSteps):
            Logger.getLogger().debug("Differenza steps sufficienti")
            self.move_curtains_steps(steps)
            # solo se la differenza è misurabile imposto le coordinate
            # precedenti uguali a quelle attuali altrimenti muovendosi
            # a piccoli movimenti le tende non verrebbero mai spostate

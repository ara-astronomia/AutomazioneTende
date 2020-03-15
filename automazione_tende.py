import time, config
from logger import Logger
from status import Status, TelescopeStatus
from typing import Dict, Any
from crac_status import CracStatus
from orientation import Orientation

class AutomazioneTende:
#(Thread):
    def __init__(self, mock: bool = False, thesky: bool = False):
#        Thread.__init__(self)
        self.mock = mock
        self.thesky = thesky
        if not mock:
            from roof_control import RoofControl
            from curtains import WestCurtain, EastCurtain
        else:
            from unittest.mock import patch, MagicMock
            from mock.roof_control import RoofControl # type: ignore
            from mock.curtains import WestCurtain, EastCurtain # type: ignore
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
        self.telescopio = telescopio.Telescopio(config.Config.getValue("theskyx_server"), config.Config.getValue('altaz_mount_file'), config.Config.getValue('park_tele_file'))
        self.curtain_east = EastCurtain()
        self.curtain_west = WestCurtain()

        self.started = False

        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")

        self.azimut_ne = config.Config.getInt("azNE", "azimut")
        self.azimut_se = config.Config.getInt("azSE", "azimut")
        self.azimut_sw = config.Config.getInt("azSW", "azimut")
        self.azimut_nw = config.Config.getInt("azNW", "azimut")

        # stabilisco il valore di increm per ogni tenda, increm corrisponde al valore dell'angolo della tenda coperto da 1 step)
        self.increm_e = (self.alt_max_tend_e - self.alt_min_tend_e) / self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w - self.alt_min_tend_w) / self.n_step_corsa

        self.crac_status = CracStatus()

    def read(self) -> CracStatus:

        """ Read the status of all CRaC components and update the CracStatus object """

        self.crac_status.roof_status = self.roof_control.read()
        self.read_altaz_mount_coordinate()
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

        return self.crac_status

    def park_tele(self) -> Dict[str, Any]:

        """ Park the Telescope """

        try:
            self.telescopio.open_connection()
            self.telescopio.park_tele()
            self.telescopio.close_connection()
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, non è possibile parcheggiare il telescopio")
        status = self.telescopio.read()
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", status, self.telescopio.coords["alt"], self.telescopio.coords["az"])
        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = status

        return self.telescopio.coords

    def read_altaz_mount_coordinate(self) -> dict:

        """ Read Telescope Coordinates """

        try:
            self.telescopio.open_connection()
            status = self.telescopio.read(update=True)
            self.telescopio.close_connection()
            Logger.getLogger().debug("Telescopio")
            Logger.getLogger().debug("Telescopio: "+str(self.telescopio.coords))
            if "error" in self.telescopio.coords:
                Logger.getLogger().debug("Errore Telescopio: "+str(self.telescopio.coords['error']))
            else:
                Logger.getLogger().debug("Altezza Telescopio: %s", str(self.telescopio.coords['alt']))
                Logger.getLogger().debug("Azimut Telescopio: %s", str(self.telescopio.coords['az']))
            Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", status, self.telescopio.coords["alt"], self.telescopio.coords["az"])
            self.crac_status.telescope_coords = self.telescopio.coords
            self.crac_status.telescope_status = status

            return self.telescopio.coords
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, per usare il mock delle coordinate telescopio NON usare il flag -s per avviare il server")
            raise

    def __convert_altitude_in_steps__(self, alt: int, orientation: Orientation):

        """ Convert an altitude in steps """

        if Orientation.EAST:
            increm = self.increm_e
        else:
            increm = self.increm_w

        return int(alt / increm)
    
    def __distance_from_telescope__(self, orientation: Orientation):

        return self.__convert_altitude_in_steps__(config.Config.getFloat("diff_alt", "tende") / 60, orientation)

    def move_curtains_height(self, coord: Dict[str, int]):

        """ Change the height of the curtains to based on the given Coordinates """

        self.crac_status.curtain_east_steps = self.__convert_altitude_in_steps__(self.crac_status.telescope_coords["alt"], Orientation.EAST)
        self.crac_status.curtain_west_steps = self.__convert_altitude_in_steps__(self.crac_status.telescope_coords["alt"], Orientation.WEST)

        if (
            self.__diff_steps__(self.crac_status.curtain_east_steps, self.crac_status.old_curtain_east_steps) or
            self.__diff_steps__(self.crac_status.curtain_west_steps, self.crac_status.old_curtain_west_steps)
        ):
            self.crac_status.old_curtain_east_steps = self.crac_status.curtain_east_steps
            self.crac_status.old_curtain_west_steps = self.crac_status.curtain_west_steps
        else:
            return

        # TODO verify tele height:
        # if less than east_min_height e ovest_min_height
        if coord["alt"] <= self.telescopio.max_secure_alt:
            #   move both curtains to 0
            self.park_curtains()
            #   else if higher than east_max_height or higher than ovest_max_height
        elif coord["alt"] >= self.alt_max_tend_e and coord["alt"] >= self.alt_max_tend_w or self.azimut_ne > coord['az'] or coord['az'] > self.azimut_nw or self.azimut_sw > coord['az'] > self.azimut_se:
            #   move both curtains max open
            self.open_all_curtains()

            #   else if higher than ovest_min_height and Az tele to west
        elif self.azimut_sw < coord["az"] <= self.azimut_nw:
            #   move curtain east max open
            self.curtain_east.open_up()
            #   if less than west_min_height
            if coord["alt"] <= self.alt_min_tend_w:
                #   move curtain west to 0 (closed)
                self.curtain_west.bring_down()
            else:
                #   move curtain west to f(Alt telescope - x)
                self.curtain_west.move(self.crac_status.curtain_west_steps - self.__distance_from_telescope__(Orientation.WEST)) # move curtain west to step

            #   else if higher than ovest_min_height and Az tele to est
        elif self.azimut_ne <= coord["az"] <= self.azimut_se:
            #   move curtian west max open
            self.curtain_west.open_up()
            #   if lower than est_min_height
            if coord["alt"] <= self.alt_min_tend_e:
                #   move curtain east to 0 (closed)
                self.curtain_east.bring_down()
            else:
                #   move curtain east to f(Alt tele - x)
                self.curtain_east.move(self.crac_status.curtain_east_steps - self.__distance_from_telescope__(Orientation.EAST)) # move curtain east to step
        
        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

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

    def diff_coordinates(self, prevCoord: Dict[str, int], coord: Dict[str, int]) -> bool:

        """ Check if delta coord is enough to move the curtains """

        Logger.getLogger().debug(coord)
        Logger.getLogger().debug(prevCoord)
        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_azi")

    def __diff_steps__(self, prev_steps: int, steps: int) -> bool:

        """ Check if delta coord is enough to move the curtains """

        Logger.getLogger().debug(steps)
        Logger.getLogger().debug(prev_steps)
        return abs(steps - prev_steps) >= config.Config.getFloat("diff_alt", "tende") / self.increm_e * 60

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

    def exit_program(self, n: int = 0) -> None:

        """ Shutdown the server """

        from gpio_config import GPIOConfig
        Logger.getLogger().info("Uscita dall'applicazione")
        self.telescopio.close_connection()
        GPIOConfig().cleanup(n)

    def exec(self) -> None:

        """ Move the curtains """

        if not self.started:
            return
        self.read()
        # current_coord = self.read_altaz_mount_coordinate()
        # if "error" not in current_coord:
        #     self.crac_status.telescope_coords = current_coord
        # Logger.getLogger().debug(self.crac_status.telescope_coords)
        # if self.diff_coordinates(self.crac_status._old_telescope_coords, self.crac_status.telescope_coords): # TODO diff between steps instead of coords
        #     self.crac_status._old_telescope_coords = self.crac_status.telescope_coords
        #     Logger.getLogger().debug(self.crac_status._old_telescope_coords)
        self.move_curtains_height(self.crac_status.telescope_coords)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tende non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep", "automazione"))

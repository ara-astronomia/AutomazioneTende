import time, config
from logger import Logger
from status import Status, TelescopeStatus
from typing import Dict, Any

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
        self.prevCoord = { 'alt': 0, 'az': 0 }

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

    def read(self):
        
        self.crac_status.roof_status = self.roof_control.read()
        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = self.telescopio.read()
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
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, non è possibile parcheggiare il telescopio")
        status = self.telescopio.read(update=False)
        Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", status, self.telescopio.coords["alt"], self.telescopio.coords["az"])
        self.crac_status.telescope_coords = self.telescopio.coords
        self.crac_status.telescope_status = self.telescopio.read()
        return self.telescopio.coords

    def read_altaz_mount_coordinate(self) -> dict:

        """ Read Telescope Coordinates """

        try:
            status = self.telescopio.read(update=True)
            Logger.getLogger().debug("Telescopio")
            Logger.getLogger().debug("Telescopio: "+str(self.telescopio.coords))
            if "error" in self.telescopio.coords:
                Logger.getLogger().debug("Errore Telescopio: "+str(self.telescopio.coords['error']))
            else:
                Logger.getLogger().debug("Altezza Telescopio: "+str(self.telescopio.coords['alt']))
                Logger.getLogger().debug("Azimut Telescopio: "+str(self.telescopio.coords['az']))
            Logger.getLogger().debug("Telescope status %s, altitude %s, azimuth %s", status, self.telescopio.coords["alt"], self.telescopio.coords["az"])
            self.crac_status.telescope_coords = self.telescopio.coords
            self.crac_status.telescope_status = status
            return self.telescopio.coords
        except ConnectionRefusedError:
            Logger.getLogger().error("Server non raggiungibile, per usare il mock delle coordinate telescopio NON usare il flag -s per avviare il server")
            raise

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

    def park_curtains(self) -> Dict[str, int]:

        """" Bring down both curtains """
        
        self.curtain_east.bring_down()
        self.curtain_west.bring_down()

        self.crac_status.curtain_east_status = self.curtain_east.read()
        self.crac_status.curtain_east_steps = self.curtain_east.steps
        self.crac_status.curtain_west_status = self.curtain_west.read()
        self.crac_status.curtain_west_steps = self.curtain_west.steps

        return { 'alt': 0, 'az': 0 }

    def open_all_curtains(self):
        
        """ Open up both curtains to the max extents """
        
        self.curtain_east.open_up()
        self.curtain_west.open_up()

    def diff_coordinates(self, prevCoord: Dict[str, int], coord: Dict[str, int]) -> bool:

        """ Check if delta coord is enough to move the curtains """
        print(coord)
        print(prevCoord)
        return abs(coord["alt"] - prevCoord["alt"]) > config.Config.getFloat("diff_al") or abs(coord["az"] - prevCoord["az"]) > config.Config.getFloat("diff_azi")

    def open_roof(self) -> bool:
        self.telescopio.open_connection()
        status_roof = self.roof_control.read()
        Logger.getLogger().info("Lo status tetto iniziale: %s ", str(status_roof))
        if status_roof != Status.OPEN:
            self.roof_control.open()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))
        
        self.crac_status.roof_status = status_roof

        return status_roof == Status.OPEN

    def close_roof(self) -> bool:
        self.telescopio.close_connection()
        status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto iniziale: %s", str(status_roof))
        if status_roof != Status.CLOSED:
            self.roof_control.close()
            status_roof = self.roof_control.read()
        Logger.getLogger().debug("Stato tetto finale: %s", str(status_roof))

        self.crac_status.roof_status = status_roof

        return status_roof == Status.CLOSED

    def exit_program(self, n: int = 0) -> None:
        from gpio_config import GPIOConfig
        Logger.getLogger().info("Uscita dall'applicazione")
        self.telescopio.close_connection()
        GPIOConfig().cleanup(n)

    def exec(self) -> int:
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
        Logger.getLogger().debug("SIAMO QUI")
        if self.diff_coordinates(self.prevCoord, self.coord):
            Logger.getLogger().debug("SIAMO QUI")
            self.prevCoord = self.coord
            Logger.getLogger().debug(self.prevCoord)
            self.move_curtains_height(self.coord)
            # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
            # altrimenti muovendosi a piccoli movimenti le tende non verrebbero mai spostate
        time.sleep(config.Config.getFloat("sleep", "automazione"))
        return 1


class CracStatus():

    def __init__(self, code=None):

        self.roof_status: Status = Status.CLOSED
        self.telescope_status: TelescopeStatus = TelescopeStatus.PARKED
        self._telescope_coords: Dict[str, str] = { "alt": "000", "az": "000" }
        self.curtain_east_status: Status = Status.CLOSED
        self._curtain_east_steps: str = "000"
        self.curtain_west_status: Status = Status.CLOSED
        self._curtain_west_steps: str = "000"
        
        if code:
            self.roof_status = Status.get_value(code[0])
            self.telescope_status = TelescopeStatus.get_value(code[1])
            self._telescope_coords = { "alt": code[2:5], "az": code[5:8] }
            self.curtain_east_status = Status.get_value(code[8])
            self._curtain_east_steps = code[9:12]
            self.curtain_west_status = Status.get_value(code[12])
            self._curtain_west_steps = code[13:16]

    def __repr__(self):
        return f'{repr(self.roof_status)}{repr(self.telescope_status)}{self.telescope_coords["alt"]}{self.telescope_coords["az"]}{repr(self.curtain_east_status)}{self.curtain_east_steps}{repr(self.curtain_west_status)}{self.curtain_west_steps}'

    @property
    def telescope_coords(self):
        return self._telescope_coords
    
    @telescope_coords.setter
    def telescope_coords(self, coords: Dict[str, int]) -> None:
        self._telescope_coords = { "alt": self.__convert_steps__(coords["alt"]), "az": self.__convert_steps__(coords["az"]) }

    @property
    def curtain_east_steps(self) -> str:
        return self._curtain_east_steps
    
    @curtain_east_steps.setter
    def curtain_east_steps(self, steps: int) -> None:
        self._curtain_east_steps = self.__convert_steps__(steps)

    @property
    def curtain_west_steps(self) -> str:
        return self._curtain_west_steps
    
    @curtain_west_steps.setter
    def curtain_west_steps(self, steps: int) -> None:
        self._curtain_west_steps = self.__convert_steps__(steps)

    def __convert_steps__(self, steps: int) -> str:
        return f'{steps:03}'

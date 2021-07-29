import unittest
import config
import socket
import datetime
from unittest.mock import DEFAULT, MagicMock
from components.telescope.simulator.telescope import Telescope
import socket
from base.singleton import Singleton


class MockTelescopeTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.telescopio = Telescope()
        socket.socket.connect = MagicMock(return_value=None)
        socket.socket.close = MagicMock(return_value=None)
        self.configGetInt = config.Config.getInt
        self.configGetFloat = config.Config.getFloat
        self.configGetValue = config.Config.getValue

    def tearDown(self):
        alt = self.telescopio.park_alt
        az = self.telescopio.park_az
        tr = 0
        self.telescopio.move_tele(alt=alt, az=az, tr=0)

    def test_connection(self):
        self.assertEqual(False, self.telescopio.connected)
        self.telescopio.open_connection()
        self.assertEqual(True, self.telescopio.connected)

    def test_close_connection(self):
        self.assertEqual(False, self.telescopio.connected)
        self.telescopio.open_connection()
        self.telescopio.close_connection()
        self.assertEqual(False, self.telescopio.connected)

    def test_read_coords(self):
        self.telescopio.update_coords(az=106.2017082212961, alt=22.049386909452107, tr=1, sl=0, error=0)
        self.assertEqual({"az": 106.20, "alt": 22.05, "tr": 1, "sl": 0, "error": 0}, self.telescopio.coords)

    def test_move_tele(self):
        self.telescopio.move_tele(sl=0, tr=0, az=0, alt=0)
        self.assertEqual(self.telescopio.coords, {"sl": 0, "tr": 0, "alt": 0, "az": 0, "error": 0})

    def __side_effect_config__(self, key, section="automazione"):
        if key == "park_alt" and section == "telescope":
            side_effect = 0.2
        elif key == "park_az" and section == "telescope":
            side_effect = 0.1
        elif key == "lat" and section == "geography":
            side_effect = "+12d48.69m"
        elif key == "lon" and section == "geography":
            side_effect = "42d13.76m"
        elif key == "height" and section == "geography":
            side_effect = 465
        elif key == "equinox" and section == "geography":
            side_effect = "J2000"
        elif key == "timezone" and section == "geography":
            side_effect = "Europe/Rome"
        elif key == "loggingLevel" and section == "automazione":
            side_effect = 10
        else:
            side_effect = DEFAULT
        return side_effect

    def test_sync_tele(self):
        date = datetime.datetime(2020, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)
        config.Config.getInt = MagicMock(side_effect=self.__side_effect_config__)
        config.Config.getFloat = MagicMock(side_effect=self.__side_effect_config__)
        config.Config.getValue = MagicMock(side_effect=self.__side_effect_config__)
        self.telescopio.sync_time = date
        coords = self.telescopio.sync()
        self.assertEqual(round(coords["ra"], 4), round(9.364493538084828, 4))
        self.assertEqual(round(coords["dec"], 4), round(47.962112290530065, 4))

    def test_radec2altaz(self):
        coords = {"ra": 9.364493538084828, "dec": 47.962112290530065}
        self.telescopio.radec2altaz(datetime.datetime(2020, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc), **coords)
        self.assertEqual(self.telescopio.coords, {"tr": 0, "sl": 0, "alt": 0, "az": 0, "error": 0})

    def tearDown(self):
        config.Config.getInt = self.configGetInt
        config.Config.getFloat = self.configGetFloat
        config.Config.getValue = self.configGetValue

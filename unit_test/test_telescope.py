import unittest
import config
import datetime
import socket
from unittest import signals
from unittest.mock import DEFAULT, MagicMock
from components.telescope.theskyx.telescope import Telescope
from base.singleton import Singleton


class TelescopeTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.telescopio = Telescope()
        socket.socket.connect = MagicMock(return_value=None)
        socket.socket.close = MagicMock(return_value=None)
        self.configGetInt = config.Config.getInt
        self.configGetFloat = config.Config.getFloat
        self.configGetValue = config.Config.getValue

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
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"tr":1,"az":106.2017082212961,"alt":22.049386909452107}|No error. Error = 0.')
        self.telescopio.update_coords()
        self.assertEqual({"az": 106.20, "alt": 22.05, "tr": 1, "error": 0}, self.telescopio.coords)

    def test_move_tele(self):
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"tr":0,"az":0,"alt":0}|No error. Error = 0.')
        self.telescopio.move_tele()
        self.assertEqual(self.telescopio.coords, {"tr": 0, "alt": 0, "az": 0, "error": 0})

    def test_parse_result_success(self):
        data = b'{"tr":1,"az":95.2017082212961,"alt":61.949386909452107}|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual({"tr": 1, "az": 95.20, "alt": 61.95, "error": 0}, self.telescopio.coords)

    def test_parse_result_error(self):
        data = b'{Error = 234.|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual(234, self.telescopio.coords["error"])

    def test_sync_tele(self):
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"tr":0,"az":0,"alt":0}|No error. Error = 0.')
        sync_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=2))
        self.telescopio.sync(sync_time)
        self.assertEqual(self.telescopio.coords, {"tr": 0, "alt": 0, "az": 0, "error": 0})

    def __side_effect_config__(self, key, section=""):
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
        elif key == "name_obs" and section == "geography":
            side_effect = "157FrassoSabino"
        elif key == "equinox" and section == "geography":
            side_effect = "J2000"
        elif key == "timezone" and section == "geography":
            side_effect = "Europe/Rome"
        else:
            side_effect = DEFAULT
        return side_effect

    def test_conv_altaz_to_ardec(self):
        from components.telescope.sync import conv_altaz_to_ardec

        date = datetime.datetime(2020, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)
        config.Config.getInt = MagicMock(side_effect=self.__side_effect_config__)
        config.Config.getFloat = MagicMock(side_effect=self.__side_effect_config__)
        config.Config.getValue = MagicMock(side_effect=self.__side_effect_config__)
        coords = conv_altaz_to_ardec(date)
        self.assertEqual(coords[0], 9.364517932878291)
        self.assertEqual(coords[1], 47.96211142851545)

    def tearDown(self):
        config.Config.getInt = self.configGetInt
        config.Config.getFloat = self.configGetFloat
        config.Config.getValue = self.configGetValue

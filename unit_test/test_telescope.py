import unittest, config
from unittest.mock import MagicMock
from telescopio import Telescopio
import socket

class TelescopeTest(unittest.TestCase):

    def setUp(self):
        self.telescopio = Telescopio(config.Config.getValue("theskyx_server"), 3040 ,config.Config.getValue('altaz_mount_file'),config.Config.getValue('park_tele_file'))

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
        self.telescopio.s.recv = MagicMock(return_value=b'{"az":106.2017082212961,"alt":22.049386909452107}|No error. Error = 0.')
        self.assertEqual({"az":106,"alt":22}, self.telescopio.coords())

    def test_park_tele(self):
        self.telescopio.open_connection()
        self.telescopio.park_tele()

    def test_parse_result_success(self):
        data = b'{"az":95.2017082212961,"alt":61.949386909452107}|No error. Error = 0.'.decode("utf-8")
        self.assertEqual({"az":95,"alt":62}, self.telescopio.__parse_result__(data))

    def test_parse_result_undefined(self):
        data = b'{undefined|No error. Error = 0.'.decode("utf-8")
        self.assertEqual({"error": True}, self.telescopio.__parse_result__(data))

    def test_parse_result_error(self):
        data = b'{undefined|Error = 1.'.decode("utf-8")
        self.assertEqual({"error": True}, self.telescopio.__parse_result__(data))

import unittest, config, socket
from unittest.mock import MagicMock
from telescopio import Telescopio
import socket
from base.singleton import Singleton

class TelescopeTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.telescopio = Telescopio(config.Config.getValue("theskyx_server") ,config.Config.getValue('altaz_mount_file'),config.Config.getValue('park_tele_file'),config.Config.getValue('flat_tele_file'), config.Config.getValue('tracking_on_tele_file'))
        socket.socket.connect = MagicMock(return_value=None)
        socket.socket.close = MagicMock(return_value=None)

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
        self.telescopio.update_coords()
        self.assertEqual({"az":106, "alt":22, "error":0}, self.telescopio.coords)

    def test_park_tele(self):
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"az":0,"alt":0}|No error. Error = 0.')
        self.telescopio.park_tele()
        self.assertEqual(self.telescopio.coords, {"alt": 0, "az": 0, "error":0})

    def test_parse_result_success(self):
        data = b'{"az":95.2017082212961,"alt":61.949386909452107}|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual({"az":95, "alt":62, "error":0}, self.telescopio.coords)

    def test_parse_result_error(self):
        data = b'{Error = 234.|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual(234, self.telescopio.coords["error"])

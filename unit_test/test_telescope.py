import unittest
import datetime
import socket
from unittest.mock import DEFAULT, MagicMock
from components.telescope.theskyx.telescope import Telescope
from base.singleton import Singleton
from astropy.utils.iers import conf


class TelescopeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conf.auto_max_age = None

    def setUp(self):
        Singleton._instances = {}
        self.telescopio = Telescope()
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
        self.telescopio.s.recv = MagicMock(return_value=b'{"sl":0,"tr":1,"az":106.2017082212961,"alt":22.049386909452107}|No error. Error = 0.')
        self.telescopio.update_coords()
        self.assertEqual({"sl": 0, "az": 106.20, "alt": 22.05, "tr": 1, "error": 0}, self.telescopio.coords)

    def test_move_tele(self):
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"tr":0,"az":0,"alt":0}|No error. Error = 0.')
        self.telescopio.move_tele()
        self.assertEqual(self.telescopio.coords, {"tr": 0, "alt": 0, "az": 0, "error": 0})

    def test_parse_result_success(self):
        data = b'{"sl":0,"tr":1,"az":95.2017082212961,"alt":61.949386909452107}|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual({"sl": 0, "tr": 1, "az": 95.20, "alt": 61.95, "error": 0}, self.telescopio.coords)

    def test_parse_result_error(self):
        data = b'{Error = 234.|No error. Error = 0.'.decode("utf-8")
        self.telescopio.__parse_result__(data)
        self.assertEqual(234, self.telescopio.coords["error"])

    def test_sync_tele(self):
        self.telescopio.open_connection()
        self.telescopio.s.recv = MagicMock(return_value=b'{"sl":0,"tr":0,"az":0,"alt":0}|No error. Error = 0.')
        sync_time = datetime.datetime.utcnow()
        self.telescopio.sync_time = sync_time
        self.telescopio.sync()
        self.assertEqual(self.telescopio.coords, {"sl": 0, "tr": 0, "alt": 0, "az": 0, "error": 0})
        # TODO check ardec coordinates given the tracking is on or off

import unittest
import config
import socket
from unittest.mock import MagicMock
from mock.telescope import Telescope
import socket
from base.singleton import Singleton


class MockTelescopeTest(unittest.TestCase):

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
        self.telescopio.update_coords(az=106.2017082212961, alt=22.049386909452107, tr=1, error=0)
        self.assertEqual({"az": 106, "alt": 22, "tr": 1, "error": 0}, self.telescopio.coords)

    def test_move_tele(self):
        self.telescopio.move_tele(tr=0, az=0, alt=0)
        self.assertEqual(self.telescopio.coords, {"tr": 0, "alt": 0, "az": 0, "error": 0})

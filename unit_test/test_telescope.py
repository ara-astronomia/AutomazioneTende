import unittest, config
from unittest.mock import MagicMock
from telescopio import Telescopio

class TelescopeTest(unittest.TestCase):

    def setUp(self):
        self.telescopio = Telescopio(config.Config.getValue("theskyx_server"), 3040 ,config.Config.getValue('altaz_mount_file'),config.Config.getValue('park_tele_file'))

    def test_connection(self):
        self.assertEqual(False, self.telescopio.connected)
        self.telescopio.open_connection()
        self.assertEqual(True, self.telescopio.connected)

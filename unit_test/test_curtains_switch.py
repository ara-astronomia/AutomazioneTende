import unittest
from curtains_switch import CurtainEastSwitch, CurtainWestSwitch
from unittest.mock import MagicMock
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from status import Status
from curtains_control import EastCurtain, WestCurtain

class CurtainSwitchTest(unittest.TestCase):

    def test_east_read_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_E_VERIFY_OPEN else False)
        switch = CurtainEastSwitch()
        self.assertEqual(switch.read(), Status.OPEN)

    def test_west_read_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_W_VERIFY_OPEN else False)
        switch = CurtainWestSwitch()
        self.assertEqual(switch.read(), Status.OPEN)

    def test_est_open(self):
        # configuration
        curtain = EastCurtain()
        curtain.open = MagicMock()
        curtain.stop = MagicMock()
        GPIOConfig.wait_for_raising = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_E_VERIFY_OPEN else False)

        # test
        switch = CurtainEastSwitch()
        switch.open()

        # check results
        curtain.open.assert_called_once()
        GPIOConfig.wait_for_raising.assert_called_once_with(GPIOPin.CURTAIN_E_VERIFY_OPEN)
        curtain.stop.assert_called_once()

    def test_west_open(self):
        # configuration
        curtain = WestCurtain()
        curtain.open = MagicMock()
        curtain.stop = MagicMock()
        GPIOConfig.wait_for_raising = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_W_VERIFY_OPEN else False)

        # test
        switch = CurtainWestSwitch()
        switch.open()

        # check results
        curtain.open.assert_called_once()
        GPIOConfig.wait_for_raising.assert_called_once_with(GPIOPin.CURTAIN_E_VERIFY_OPEN)
        curtain.stop.assert_called_once()

    def test_est_close(self):
        # configuration
        curtain = EastCurtain()
        curtain.close = MagicMock()
        curtain.stop = MagicMock()
        GPIOConfig.wait_for_raising = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_E_VERIFY_CLOSED else False)

        # test
        switch = CurtainEastSwitch()
        switch.close()

        # check results
        curtain.close.assert_called_once()
        GPIOConfig.wait_for_raising.assert_called_once_with(GPIOPin.CLOSED)
        curtain.stop.assert_called_once()

    def test_west_close(self):
        # configuration
        curtain = WestCurtain()
        curtain.close = MagicMock()
        curtain.stop = MagicMock()
        GPIOConfig.wait_for_raising = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_W_VERIFY_CLOSED else False)

        # test
        switch = CurtainWestSwitch()
        switch.close()

        # check results
        curtain.close.assert_called_once()
        GPIOConfig.wait_for_raising.assert_called_once_with(GPIOPin.CLOSED)
        curtain.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()

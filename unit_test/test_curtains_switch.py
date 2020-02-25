import unittest
from curtains_switch import CurtainEastSwitch, CurtainWestSwitch
from unittest.mock import MagicMock
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from status import Status

class CurtainSwitchTest(unittest.TestCase):
    def test_est_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_E_VERIFY_OPEN else False)
        switch = CurtainEastSwitch()
        switch.open()
        self.assertEqual(switch.read(), Status.OPEN)

    def test_west_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.CURTAIN_W_VERIFY_OPEN else False)
        switch = CurtainWestSwitch()
        switch.open()
        self.assertEqual(switch.read(), Status.OPEN)

    # def test_est_close(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_B or value == GPIOPin.MOTORE_E else False)
    #     encoder = EastEncoder()
    #     encoder.steps = 10
    #     encoder.move(5)
    #
    # def test_west_close(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_B or value == GPIOPin.MOTORW_E else False)
    #     encoder = WestEncoder()
    #     encoder.steps = 10
    #     encoder.move(5)
    #
    # def test_count_step(self):
    #     encoder = WestEncoder()
    #     encoder.target = 100
    #     encoder.__count_steps__()
    #     self.assertEqual(1, encoder.steps)
    #
    # def test_count_step_back(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: value != GPIOPin.CLK_E)
    #     encoder = WestEncoder()
    #     encoder.steps = 5
    #     encoder.target = 1
    #     encoder.__count_steps__()
    #     self.assertEqual(4, encoder.steps)

if __name__ == '__main__':
    unittest.main()

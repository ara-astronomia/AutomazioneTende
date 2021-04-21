import unittest
import config
import socket
from unittest.mock import DEFAULT, MagicMock
from automazione_tende import AutomazioneTende
import socket
from base.singleton import Singleton
from status import TelescopeStatus


class AutomazioneTendeTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.original_config_getInt = config.Config.getInt
        self.automazioneTende = AutomazioneTende(telescope_plugin="theskyx")

    def __side_effect_for_diff_steps__(self, key, section=""):
        if key == "diff_steps" and section == "encoder_step":
            side_effect = 0
        else:
            side_effect = DEFAULT
        return side_effect

    def test_is_diff_steps_enough(self):
        config.Config.getInt = MagicMock(side_effect=self.__side_effect_for_diff_steps__)
        cs = {"east": 100, "west": 50}
        ps = {"east": 90, "west": 50}
        self.assertTrue(self.automazioneTende.is_diff_steps(cs, ps))

    def test_is_diff_steps_not_enough(self):
        config.Config.getInt = MagicMock(side_effect=self.__side_effect_for_diff_steps__)
        cs = {"east": 100, "west": 50}
        self.assertFalse(self.automazioneTende.is_diff_steps(cs, cs))

    def test_calculate_curtains_step_tele_in_error(self):
        telescopio = MagicMock()
        at = self.automazioneTende
        at.telescope = telescopio
        comparison = {"east": at.curtain_east.steps(), "west": at.curtain_west.steps()}

        telescopio.status = TelescopeStatus.ERROR
        steps = at.calculate_curtains_steps()
        self.assertEqual(steps, comparison)

        telescopio.status = TelescopeStatus.LOST
        steps = at.calculate_curtains_steps()
        self.assertEqual(steps, comparison)

    def test_calculate_curtains_steps_at_min(self):
        telescopio = MagicMock()
        telescopio.is_below_curtains_area = MagicMock(return_value=True)
        at = self.automazioneTende
        at.telescope = telescopio
        steps = at.calculate_curtains_steps()
        comparison = {"east": at.alt_min_tend_e, "west": at.alt_min_tend_w}
        self.assertEqual(steps, comparison)

    def test_calculate_curtains_steps_at_max(self):
        telescopio = MagicMock()
        telescopio.is_below_curtains_area = MagicMock(return_value=False)
        telescopio.is_above_curtains_area = MagicMock(return_value=True)
        at = self.automazioneTende
        at.telescope = telescopio
        steps = at.calculate_curtains_steps()
        comparison = {"east": at.n_step_corsa, "west": at.n_step_corsa}
        self.assertEqual(steps, comparison)

    def test_calculate_curtains_steps_at_east_max(self):
        telescopio = MagicMock()
        telescopio.is_below_curtains_area = MagicMock(return_value=False)
        telescopio.is_above_curtains_area = MagicMock(return_value=False)
        telescopio.is_within_curtains_area = MagicMock(return_value=True)
        telescopio.status = TelescopeStatus.WEST
        telescopio.coords = {"alt": 40.0}
        at = self.automazioneTende
        at.telescope = telescopio
        steps = at.calculate_curtains_steps()
        comparison = {"east": at.n_step_corsa, "west": 200}
        self.assertEqual(steps, comparison)

    def test_calculate_curtains_steps_at_west_max(self):
        telescopio = MagicMock()
        telescopio.is_below_curtains_area = MagicMock(return_value=False)
        telescopio.is_above_curtains_area = MagicMock(return_value=False)
        telescopio.is_within_curtains_area = MagicMock(return_value=True)
        telescopio.status = TelescopeStatus.EAST
        telescopio.coords = {"alt": 40.0}
        at = self.automazioneTende
        at.telescope = telescopio
        steps = at.calculate_curtains_steps()
        comparison = {"east": 200, "west": at.n_step_corsa}
        self.assertEqual(steps, comparison)

    def tearDown(self):
        config.Config.getInt = self.original_config_getInt

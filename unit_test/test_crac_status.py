import unittest
from crac_status import CracStatus
from status import Status, TelescopeStatus, CurtainsStatus


class TestCracStatus(unittest.TestCase):

    def test_is_in_anomaly(self):
        cs = CracStatus()
        cs.curtain_east_status = CurtainsStatus.STOPPED
        self.assertTrue(cs.is_in_anomaly())

    def test_are_in_danger(self):
        cs = CracStatus()
        cs.curtain_east_status = CurtainsStatus.DANGER
        self.assertTrue(cs.are_curtains_in_danger())

    def test_are_closed(self):
        cs = CracStatus()
        cs.curtain_east_status = CurtainsStatus.DISABLED
        cs.curtain_west_status = CurtainsStatus.DISABLED
        self.assertTrue(cs.are_curtains_disabled())

    def test_telescope_in_secure_and_roof_is_closed(self):
        cs = CracStatus()
        cs.telescope_status = TelescopeStatus.SECURE
        cs.roof_status = Status.CLOSED
        self.assertTrue(cs.telescope_in_secure_and_roof_is_closed)

    def test_telescope_in_secure_and_roof_is_closing(self):
        cs = CracStatus()
        cs.telescope_status = TelescopeStatus.SECURE
        cs.roof_status = Status.CLOSING
        self.assertTrue(cs.telescope_in_secure_and_roof_is_closing)

    def test_create_crac_status(self):
        code = "CPP0802012534A250S090SSSAAS"
        cs = CracStatus(code)
        self.assertEqual(cs.telescope_coords, {"alt": 80.20, "az": 125.34})
        self.assertEqual(repr(cs), code)

    def test_create_crac_status_2(self):
        code = "OSS-036100992C000C000TSASSN"
        cs = CracStatus(code)
        self.assertEqual(cs.telescope_coords, {"alt": -3.61, "az": 9.92})
        self.assertEqual(repr(cs), code)

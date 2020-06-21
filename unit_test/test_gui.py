from gui import Gui
import unittest
from unittest.mock import MagicMock, patch
from status import Orientation
import config


class TestGui(unittest.TestCase):

    def setUp(self):
        self.gui = Gui()

    def test_create_polygon_coordinates_with_est_low(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(0, Orientation.EAST)

        self.assertEqual((263, 144), pt)
        self.assertEqual((352, 163), pt1)
        self.assertEqual((352, 163), pt2)
        self.assertEqual((352, 163), pt3)
        self.assertEqual((352, 163), pt4)
        self.assertEqual((352, 163), pt5)

    def test_create_polygon_coordinates_with_est_middle(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(23, Orientation.EAST)

        self.assertEqual((263, 144), pt)
        self.assertEqual((352, 163), pt1)
        self.assertEqual((354, 153), pt2)
        self.assertEqual((354, 144), pt3)
        self.assertEqual((354, 136), pt4)
        self.assertEqual((353, 127), pt5)

    def test_create_polygon_coordinates_with_est_middle_1(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(70, Orientation.EAST)

        self.assertEqual((263, 144), pt)
        self.assertEqual((352, 163), pt1)
        self.assertEqual((354, 136), pt2)
        self.assertEqual((347, 109), pt3)
        self.assertEqual((332, 85), pt4)
        self.assertEqual((311, 67), pt5)

    def test_create_polygon_coordinates_with_eest_max(self):
        max_step = config.Config.getInt("n_step_corsa", "encoder_step")
        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(max_step, Orientation.EAST)

        self.assertEqual((263, 144), pt)
        self.assertEqual((352, 163), pt1)
        self.assertEqual((285, 56), pt2)
        self.assertEqual((176, 118), pt3)
        self.assertEqual((233, 230), pt4)
        self.assertEqual((348, 178), pt5)

    def test_create_polygon_coordinates_with_west_low(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(0, Orientation.WEST)

        self.assertEqual((126, 144), pt)
        self.assertEqual((37, 163), pt1)
        self.assertEqual((37, 163), pt2)
        self.assertEqual((37, 163), pt3)
        self.assertEqual((37, 163), pt4)
        self.assertEqual((37, 163), pt5)

    def test_create_polygon_coordinates_with_west_middle(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(23, Orientation.WEST)

        self.assertEqual((126, 144), pt)
        self.assertEqual((37, 163), pt1)
        self.assertEqual((35, 153), pt2)
        self.assertEqual((35, 144), pt3)
        self.assertEqual((35, 136), pt4)
        self.assertEqual((36, 127), pt5)

    def test_create_polygon_coordinates_with_west_middle_1(self):

        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(70, Orientation.WEST)

        self.assertEqual((126, 144), pt)
        self.assertEqual((37, 163), pt1)
        self.assertEqual((35, 136), pt2)
        self.assertEqual((42, 109), pt3)
        self.assertEqual((57, 85), pt4)
        self.assertEqual((78, 67), pt5)

    def test_create_polygon_coordinates_with_west_max(self):
        max_step = config.Config.getInt("n_step_corsa", "encoder_step")
        pt, pt1, pt2, pt3, pt4, pt5 = self.gui.__create_polygon_coordinates__(max_step, Orientation.WEST)

        self.assertEqual((126, 144), pt)
        self.assertEqual((37, 163), pt1)
        self.assertEqual((104, 56), pt2)
        self.assertEqual((213, 118), pt3)
        self.assertEqual((156, 230), pt4)
        self.assertEqual((41, 178), pt5)

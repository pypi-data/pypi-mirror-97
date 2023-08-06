import unittest

import numpy as np
from alloy.math import * 

import pytest

@pytest.mark.parametrize("input", [0,1,1.05,-1,-1.78,np.pi,-np.pi+0.00001])
def test_radian_clipping_equal(input):
    assert input == clip_radian_rotation(input)

@pytest.mark.parametrize("input, expected", [(np.pi + 0.5, -np.pi + 0.5), (-np.pi - 0.5, np.pi - 0.5), (np.pi*10 + 1.4, 1.4), (-np.pi*10 + 0.87, 0.87)])
def test_radian_clipping_clipped(input, expected):
    assert pytest.approx(clip_radian_rotation(input),expected)

class TestRotation2DFunction(unittest.TestCase):


    def test_degree_to_theta(self):

        # handle positive
        self.assertAlmostEqual(deg_to_theta(0), 0.0, places=6)
        self.assertAlmostEqual(deg_to_theta(90), np.pi/2, places=6)
        self.assertAlmostEqual(deg_to_theta(180), np.pi,  places=6)
        self.assertAlmostEqual(deg_to_theta(270), -np.pi/2,  places=6)
        self.assertAlmostEqual(deg_to_theta(360), 0.0, places=6)

        # handle negatives
        self.assertAlmostEqual(deg_to_theta(-90), -np.pi/2, places=6)
        self.assertAlmostEqual(deg_to_theta(-180), np.pi,  places=6)
        self.assertAlmostEqual(deg_to_theta(-270), np.pi/2,  places=6)
        self.assertAlmostEqual(deg_to_theta(-360), 0.0, places=6)       

        # test with additional revolutions
        self.assertAlmostEqual(deg_to_theta(90 + 360), np.pi/2, places=6)
        self.assertAlmostEqual(deg_to_theta(-180 - 360*2), np.pi,  places=6)

    def test_theta_to_clock(self):
        # test the four directions
        self.assertEqual(theta_to_clock(0), 12)
        self.assertEqual(theta_to_clock(np.pi), 6)
        self.assertEqual(theta_to_clock(-np.pi), 6)
        self.assertEqual(theta_to_clock(-np.pi/2), 3)
        self.assertEqual(theta_to_clock(np.pi/2), 9)

        # test some convert cases
        self.assertEqual(theta_to_clock(np.pi + 0.01), 6)
        self.assertEqual(theta_to_clock(-np.pi/2 - 0.1), 3)

    def test_find_theta_distance(self):
        # check itself
        self.assertAlmostEqual(find_theta_distance(0,0), 0 ,places=6)
        self.assertAlmostEqual(find_theta_distance(2,2), 0 ,places=6)

        # check directions
        self.assertAlmostEqual(find_theta_distance(0,1), 1 ,places=6)
        self.assertAlmostEqual(find_theta_distance(1,2), 1 ,places=6)
        self.assertAlmostEqual(find_theta_distance(0,-1), -1 ,places=6)
        self.assertAlmostEqual(find_theta_distance(-0.5,-1.5), -1 ,places=6)

        # check cross zero cases
        self.assertAlmostEqual(find_theta_distance(-2,2),((np.pi-2)*2) ,places=6)

        # check edge cases
        self.assertAlmostEqual(find_theta_distance(0, np.pi), np.pi,places=6)
        self.assertAlmostEqual(find_theta_distance(-np.pi/2, np.pi/2), np.pi,places=6)


        

    def test_find_rotation(self):

        # test with unit vectors:
        self.assertAlmostEqual(find_rotation(np.array([1, 0]), np.array([0, -1])), -np.pi/2,  places=6)
        self.assertAlmostEqual(find_rotation(np.array([1, 0]), np.array([0, 1])), np.pi/2,  places=6)
        self.assertAlmostEqual(find_rotation(np.array([1, 0]), np.array([1, 0])), 0,  places=6)
        self.assertAlmostEqual(find_rotation(np.array([1, 0]), np.array([-1, 0])), np.pi,  places=6)
        self.assertAlmostEqual(find_rotation(np.array([0, -1]), np.array([-1, 0])), -np.pi/2,  places=6)



if __name__ == '__main__':
    unittest.main()

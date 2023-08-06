import unittest

import numpy as np
from alloy.spatial.primitives import (
    Box,
    Line,
    Ray
)

class TestSpatialFunction(unittest.TestCase):

    def test_box_creation(self):
        box = Box([0,-1,-2], [1,1,1])
        self.assertEqual(box.length, 1)
        self.assertEqual(box.width, 2)
        self.assertEqual(box.height, 3)

        box2 = Box(5,5,5,1,5,6)
        self.assertEqual(box2.half_extents[2], 3)
        self.assertEqual(box2.half_extents[1], 2.5)

    def test_box_creation_center(self):
        box = Box([5,5,0],[6,6,1])
        self.assertEqual(box.center[0], 5.5)
        self.assertEqual(box.center[1], 5.5)
        self.assertEqual(box.center[2], 0.5)

    def test_box_point_intercept(self):
        
        box1 = Box(5,5,5,2,2,2)
        d, p = box1.distance_from_point([5,5,5])
        self.assertEqual(d, 0)
        np.testing.assert_array_equal(p, np.array([5,5,5]))

        d, p = box1.distance_from_point([6,6,6])
        self.assertEqual(d, 0)
        np.testing.assert_array_equal(p, np.array([6,6,6]))

        d, p = box1.distance_from_point([7,6,6])
        self.assertEqual(d, 1)
        np.testing.assert_array_equal(p, np.array([6,6,6]))

        d, p = box1.distance_from_point([4,2,4])
        self.assertEqual(d, 2)
        np.testing.assert_array_equal(p, np.array([4,4,4]))

    def test_box_contain_points(self):
        box1 = Box(0,0,0,2,2,2)
        # test center
        self.assertTrue(box1.contains_point(np.array([0,0,0])))
        # test edges
        self.assertTrue(box1.contains_point(np.array([0,1,0])))
        self.assertTrue(box1.contains_point(np.array([0,1,1])))
        self.assertTrue(box1.contains_point(np.array([0,0.5,1])))
        self.assertTrue(box1.contains_point(np.array([0.5,1,1])))
        # test negatives
        self.assertTrue(box1.contains_point(np.array([-0.5,-1,-1])))
        self.assertTrue(box1.contains_point(np.array([0.5,-0.5,0.5])))
        # test out of bounds
        self.assertFalse(box1.contains_point(np.array([0.5,0.5,2])))
        self.assertFalse(box1.contains_point(np.array([0,0,2])))
        self.assertFalse(box1.contains_point(np.array([0,0,-2])))
        # test non-center box
        box2 = Box(100,5,10,5,5,5)
        self.assertFalse(box2.contains_point(np.array([0,0,0])))
        self.assertFalse(box2.contains_point(np.array([60,10,20])))
        self.assertFalse(box2.contains_point(np.array([100,5,-20])))     
        self.assertFalse(box2.contains_point(np.array([100,5,12.6])))    

        self.assertTrue(box2.contains_point(np.array([100,5,10])))   
        self.assertTrue(box2.contains_point(np.array([102.5,5,12.5])))   
        self.assertTrue(box2.contains_point(np.array([97.5,2.5,12.5])))   



    def test_box_line_distance(self):
        box1 = Box(0,0,0,2,2,2)
        line1 = Line((0,0,0),(1,0,0))
        # inside the box
        d, proj, on_line = box1.distance_from_line(line1)
        self.assertTrue(box1.contains_point(proj))
        self.assertEqual(d, 0)
        # outside the box but on the surface
        line2 = Line((1,0,0),(1,1,0))
        d, proj, on_line = box1.distance_from_line(line1)
        self.assertTrue(box1.contains_point(proj))
        self.assertEqual(d, 0)
        # parrallel but not connected 
        d, proj, on_line = box1.distance_from_line(Line((0,5,0), (1,0,1)))
        self.assertTrue(box1.contains_point(proj))
        self.assertEqual(d, 4)
        d, proj, on_line = box1.distance_from_line(Line((0,-5,0), (1,0,1)))
        self.assertTrue(box1.contains_point(proj))
        self.assertEqual(d, 4)
        d, proj, on_line = box1.distance_from_line(Line((0,-10,0), (1,0,2)))
        self.assertTrue(box1.contains_point(proj))
        self.assertEqual(d, 9)

        # # non-zero line with that are not connected
        d, proj, on_line = box1.distance_from_line(Line((10,10,10), (-5,1,1)))
        self.assertTrue(box1.contains_point(proj))
        self.assertNotEqual(d, 0.0)

        box2 = Box(10,0,10,5,5,5)
        d, proj, on_line = box2.distance_from_line(Line((10,0,0), (1,1,1)))
        self.assertTrue(box2.contains_point(proj))
        self.assertNotEqual(d, 0.0)

        # # # # non-zero box
        box3 = Box(-10,100,20,5,5,5)
        #inside the box
        d, proj, on_line = box3.distance_from_line(Line((-10,100,20), (1,2,1)))
        self.assertTrue(box3.contains_point(proj))
        self.assertEqual(d, 0)






if __name__ == '__main__':
    unittest.main()

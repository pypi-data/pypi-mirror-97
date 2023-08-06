# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License


import unittest
from alloy.algo import depth_first_search, breath_first_search

class TestSpatialFunction(unittest.TestCase):

    def fake_child_func(self, curr_tuple):
        # The curr_tuple is (x,y)
        # The graphic starts with (0,0) and
        # goes upwards (y+1) if -1,0,+1 X
        # max size of 10
        x = curr_tuple[0]
        y = curr_tuple[1] + 1
        if (y > 10):
            return []
        else:
            return [(x-1,y),(x,y),(x+1,y)]

    def test_breath_first_search(self):
        print(breath_first_search((0,0),(2,3), self.fake_child_func))
        print(depth_first_search((0,0),(2,3), self.fake_child_func))


if __name__ == '__main__':
    unittest.main()

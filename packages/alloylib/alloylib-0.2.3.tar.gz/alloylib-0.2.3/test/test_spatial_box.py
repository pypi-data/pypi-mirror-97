import pytest
from alloy.spatial.primitives import Box
import numpy as np 


def test_box_inflated_new():
    # make sure the box is a new box
    old_box = Box([0,0,0],[1,1,1])
    new_box = Box.inflate_box(old_box,0.5,0.5,0)
    assert old_box.length == 1
    assert old_box.width == 1
    assert new_box.length == 1.5
    assert new_box.width == 1.5


def test_empty_inflated_box():
    ori_box = Box([0,0,0], [1,1,1])
    new_box = Box.inflate_box(ori_box, 0,0,0)
    assert new_box.length == 1
    assert new_box.width == 1
    assert new_box.height == 1

def test_box_deflation():
    old_box = Box([1,1,0],[2,2,1])
    new_box = Box.inflate_box(old_box,-0.5,-0.5,0)
    assert new_box.length == 0.5
    assert new_box.width == 0.5

def test_in_box_two():
    box1 = Box(0.025, 5, 0.73, 0.3, 0.28, 1.46)
    assert not box1.contains_point([0, 0, 0])
    assert box1.contains_point([0, 5, 0])
    assert box1.contains_point([0.1, 5.1, 0])
    assert not box1.contains_point([0.2, 5.2, 0])
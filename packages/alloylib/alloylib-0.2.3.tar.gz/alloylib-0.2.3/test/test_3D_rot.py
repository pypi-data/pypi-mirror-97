
import pytest
from alloy.math import rpy_to_quaternion
import numpy as np

def test_rpy_to_quaternion():
    # test zero initialization
    assert rpy_to_quaternion(0,0,0).tolist() == [1,0,0,0]

    # test roll pitch yaw by themselves
    np.testing.assert_array_almost_equal(rpy_to_quaternion(np.pi,0,0), [0,1,0,0])
    np.testing.assert_array_almost_equal(rpy_to_quaternion(0,np.pi,0), [0,0,1,0])
    np.testing.assert_array_almost_equal(rpy_to_quaternion(0,0,np.pi), [0,0,0,1])

    # test directional
    np.testing.assert_array_almost_equal(rpy_to_quaternion(np.pi/2,0,0), [0.7071068,0.7071068,0,0])
    np.testing.assert_array_almost_equal(rpy_to_quaternion(-np.pi/2,0,0), [0.7071068,-0.7071068,0,0])

    # test compounded transformation
    np.testing.assert_array_almost_equal(rpy_to_quaternion(np.pi/2,np.pi/2,0), [0.5,0.5, 0.5, 0.5])
    np.testing.assert_array_almost_equal(rpy_to_quaternion(0,np.pi/3,np.pi/6), [0.8365163, 0.1294095, 0.4829629, 0.2241439])


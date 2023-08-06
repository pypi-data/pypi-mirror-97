# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
3D(R^3) Vector operations
"""
import numpy as np
import typing 
from pyquaternion import Quaternion
from .basic import *

__all__ = ['skew_symmetric_matrix', 'rotation_matrix_from_axis_angle', 'axis_angles_from_rotation_matrix',
           'transformation_matrix_from_array', 'inverse_transformation_matrix', 'ypr_from_quaterion',
           'rot2D_from_quaternion','transformation_matrix_to_array','rpy_to_quaternion'
           ]


def skew_symmetric_matrix(vec):
    """
    Return a 3x3 skew symmetric matrix from the given vector

    parameters:
    -----------
    vec : numpy array(3,)
        vector array with three elements (x, y, z)

    returns:
    --------
    numpy array(3,3)
        the skew symmetric matrix from the given vector
    """
    matrix = [
        [0, -vec[2], vec[1]],
        [vec[2], 0, -vec[0]],
        [-vec[1], vec[0], 0]
    ]
    return np.array(matrix)


def rotation_matrix_from_axis_angle(axis, theta):
    """
    Given an axis and angle(in radian), return the rotation matrix that
    represent the that rotation of theta around given axis.

    Notes
    -----
    This is similar to the exponential rotation(R = exp(\omega_hat,theta)) as it uses the Rodrigues formula,
    where \omega_hat is the skew symmetric matrix of the axis and theta is the rotation.
    """
    if np.shape(axis) != (3,):
        raise AttributeError('Axis is incorrect size, must be (3,)')
    axis_hat = skew_symmetric_matrix(axis)
    # from page 28 of MLS 1994
    return np.eye(3) + axis_hat * np.sin(theta) + axis_hat.dot(axis_hat) * (1 - np.cos(theta))


def axis_angles_from_rotation_matrix(rot_mat):
    """Convert the rotation matrix into axis angle format
    """

    # FASTER WAY: http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToAngle/

    # SLOWER WAY
    q = Quaternion(matrix=rot_mat)
    return q.axis, q.angle


def transformation_matrix_from_array(arr):
    """Create a 3D Transformation matrix from an array that has 7 elements. 
    The first three elements is the [x,y,z] of the translation, the next four
    is the [w, x, y, z] is the quaternion that describes the rotation. 
    """
    trans = np.eye(4)
    trans[0:3, 3] = arr[:3]  # put in the transformation components
    quaternion = Quaternion(arr[3:])  # make quaternions
    trans[0:3, 0:3] = quaternion.rotation_matrix
    return trans

def transformation_matrix_to_array(mat):
    arr = np.zeros((7,))
    quaternion = Quaternion(matrix=mat[0:3,0:3])
    arr[0:3] = mat[0:3,3]
    arr[3] = quaternion.w
    arr[4] = quaternion.x
    arr[5] = quaternion.y
    arr[6] = quaternion.z
    return arr


def ypr_from_quaterion(arr):
    """Calculate the yaw,pitch,roll from a numpy quaternion [w,x,y,z]
    """
    quaternion = Quaternion(arr)
    yaw, pitch, roll = quaternion.yaw_pitch_roll
    return yaw, pitch, roll

def rpy_to_quaternion(roll:float = 0, pitch:float = 0, yaw: float = 0) -> typing.List[float]:
    """ Get a quaternion [w,x,y,z] that encodes the rotation along the 3 principle axis. The rotations
    are intrinsic in which the Y-axis for pitch is the transformed Y-axis instead of the original Y-axis.
    The operations is first transform by roll, then pitch, and finally yaw.

    Args:
        roll (float, optional): Radian around X-Axis. Defaults to 0.
        pitch (float, optional): Radian around Y-Axis. Defaults to 0.
        yaw (float, optional): Radian around Z-Axis. Defaults to 0.

    Returns:
        typing.List[float]: An array [w,x,y,z] that describe the quaternion
    """
    quaternion = Quaternion(axis=[1,0,0], radians=roll) * Quaternion(axis=[0,1,0], radians=pitch) * Quaternion(axis=[0,0,1], radians=yaw)
    return quaternion.normalised.elements
    yaw, pitch, roll = quaternion.yaw_pitch_roll
    return yaw, pitch, roll



def rot2D_from_quaternion(arr):
    """ Calculate the 2D rotation (yaw) from a numpy quaternion [w,x,y,z]
    """
    yaw, pitch, roll = ypr_from_quaterion(arr)
    return yaw


def inverse_transformation_matrix(m: np.array) -> np.array:
    """Find the inverse of a 3D transformation matrix (4,4), T from the given matrix M, such that
    x = T * (M * x)

    Parameters
    ----------
    m : np.array
        The original transformation matrix

    Returns
    -------
    np.array
        The inverse of the transformation matrix
    """

    inv_rot = (m[0:3, 0:3]).T
    inv_m = np.eye(4)
    inv_m[0:3, 3] = -1 * (inv_rot.dot(m[0:3, 3]))
    inv_m[0:3, 0:3] = inv_rot
    return inv_m

def main():
    # skew symmetric test
    # print(skew_symmetric_matrix(np.array([1,2,3])))
    # vec1 = np.array([0,1,0])
    # vec2 = np.array([1,0,0])
    # skew1 = skew_symmetric_matrix(vec1)
    # print(skew1.dot(vec2)) # [0,0,-1]
    print(transformation_matrix_from_array(
        np.array([10, 20, 300, 0.707, 0.707, 0, 0])))

    # matrix test
    # m1 = transformation_matrix_from_array(np.array([10,20,30,0.707,0.707,0,0]))
    # #m1 = transformation_matrix_from_array(np.array([10,20,30,1,0,0,0]))
    # p1 = np.array([1,5,1,1])
    # trans_p1 = m1.dot(p1)
    # print(trans_p1)
    # inv_m1 = inverse_transformation_matrix(m1)
    # ori_p1 = inv_m1.dot(trans_p1)
    # print(ori_p1)


if __name__ == '__main__':
    main()

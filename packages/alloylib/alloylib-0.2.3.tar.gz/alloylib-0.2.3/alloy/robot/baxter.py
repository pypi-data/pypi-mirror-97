# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Common Operations/Codes that are re-written on Baxter
"""

import numpy as np
from pyquaternion import Quaternion
from alloy.math import *

__all__ = [
    'convert_joint_angles_to_numpy','transform_pose_into_rotation_matrix',
    'calculate_pose_difference'
]

def convert_joint_angles_to_numpy(joint_angles, joint_names):
    """Convert the dictionary based joint angles given by baxter interface to
    a numpy array according to the given joint names
    """
    
    arr = np.zeros(7)
    for i, key in enumerate(joint_names):
        arr[i] = joint_angles[key]
    return arr

def transform_pose_into_rotation_matrix(pose_np):
    #pose_np = pose_to_numpy(pose)
    translation_comp = pose_np[0:3]
    trans_mat = Quaternion(pose_np[3:]).transformation_matrix
    trans_mat[0:3,3] = translation_comp
    return trans_mat


def calculate_pose_difference(p1, p2):
    """Calculate the pose error from p1 to p2. Note the resulting
    error is calculated in the frame of p1 and not the base frame
    do p[0:3] = p[0:3] - np.cross(x[0:3],p[3:])
    """

    error = np.zeros(6,)
    #the position error is just the difference in position
    error[0:3] = p2[0:3] - p1[0:3]
    #orientation error is more tricky
    desire_q = Quaternion(p2[3:])
    error_q = desire_q * Quaternion(p1[3:]).inverse
    error[3:] = error_q.axis * error_q.angle
    
    return error
    #transform_quaternion = Quaternion(pose_np[3:]).  Quaternion(pose_np[3:])

# def calculate_pose_difference(p1, p2):
#     """Calculate the error from p1 to p2. Note the resulting
#     error is calculated in the frame of p1 and not the base frame
#     do p[0:3] = p[0:3] - np.cross(x[0:3],p[3:])
#     """

#     mat1 = transform_pose_into_rotation_matrix(p1)
#     mat2 = transform_pose_into_rotation_matrix(p2)

#     error = calculate_error_between_two_transformation_matrix(mat1, mat2)
#     return calculate_error_between_two_transformation_matrix(mat1, mat2)

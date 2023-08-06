import numpy as np
import alloy.math
import alloy.ros

from geometry_msgs.msg import(
    Pose,
    Point,
    Transform
)

__all__ = [
    'do_transform_point',
    'do_transform_pose'
]

def do_transform_point(transform: Transform, point: Point) -> Point:
    """An implementation of the tf2_geometry_msgs interface to get around PyKDL.
    Transform a point with the given transform message.

    Parameters
    ----------
    transform : geometry_msgs/Transform
        Message that describes the transform
    point : geometry_msgs/Point
        The point to be transformed

    Returns
    -------
    geometry_msgs/Point
        Transformed point
    """

    transform_mat = alloy.math.transformation_matrix_from_array(alloy.ros.transform_to_numpy(transform))
    point_np = alloy.ros.point_to_numpy(point)
    point_np = np.append(point_np, 1).reshape((4,1))
    trans_point = np.matmul(transform_mat, point_np)
    return alloy.ros.numpy_to_point(trans_point[0:3,0])

def do_transform_pose(transform: Transform, pose: Pose) -> Pose:
    """An implementation of the tf2_geometry_msgs interface to get around PyKDL.
    Transform a pose with the given transform message.

    Parameters
    ----------
    transform : geometry_msgs/Transform
        Message that describes the transform
    pose : geometry_msgs/Pose
        The pose to be transformed

    Returns
    -------
    geometry_msgs/Pose
        Transformed pose.
    """
    transform_mat = alloy.math.transformation_matrix_from_array(alloy.ros.transform_to_numpy(transform))
    pose_mat = alloy.math.transformation_matrix_from_array(alloy.ros.pose_to_numpy(pose))
    #combine two transformation matrix
    trans_pose_mat = np.matmul(transform_mat, pose_mat)

    return alloy.ros.numpy_to_pose(alloy.math.transformation_matrix_to_array(trans_pose_mat))

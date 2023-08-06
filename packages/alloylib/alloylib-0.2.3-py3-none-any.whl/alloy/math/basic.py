# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Basic Math Operations that wraps around numpy
"""

import numpy as np

__all__ = [
    'distance', 'is_close', 'is_same', 'normalize'
]


def distance(p1, p2):
    """
    Return the euclidean distance between the two points

    parameters
    ----------
    p1 : numpy array
        N-array describing the position of p1
    p2 : numpy array
        N-array describing the position of p2
    """
    squared_dist = (p2 - p1)**2
    sum_squared = np.sum(squared_dist)
    return np.sqrt(sum_squared)


def is_close(p1, p2, limit=1e-3):
    """
    Return true if p1 and p2 is closer than the defined limit (default 1e-3)
    according to euclidean distance. False underwise

    parameters
    ----------
    p1 : numpy array
        N-array describing the position of p1
    p2 : numpy array
        N-array describing the position of p2
    limit : float (optional)
        The maximum distance p1 is allowed to be away from p2

    returns
    -------
    bool
        Whether the two points are close
    """
    return distance(p1, p2) <= limit


def is_same(p1, p2):
    """
    Return true if p1 and p2 is at the same position according to euclidean distance. False underwise

    parameters
    ----------
    p1 : numpy array
        N-array describing the position of p1
    p2 : numpy array
        N-array describing the position of p2

    returns
    -------
    bool
        Whether the two points are at the same position
    """
    return is_close(p1, p2, limit=0)


def normalize(vec):
    """
    Normalize the given vector

    parameters
    ----------
    vec : numpy array
        Vector to be normalized
    """
    return vec/np.linalg.norm(vec)


def bezier_curve(t, points):
    """
    Returns the point on the bezier curve defined by the given points and parameterized between [0,1]

    #TODO Might only work in 1D

    parameters
    ---------
    t : float
        The current point on the line. Defined as a real number between [0,1] where 0 is the beginning points and 1 is the ending
    points: numpy array of the points
        Control points that define the bezier curve
    """

    if len(points == 1):
        return points[0]

    return bezier_curve(t, points[:-1]) * (1 - t) + bezier_curve(t, points[1:]) * t

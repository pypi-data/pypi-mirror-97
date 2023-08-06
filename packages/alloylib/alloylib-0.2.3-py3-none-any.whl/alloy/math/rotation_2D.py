# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Common 2D Rotation Operations
"""

from .basic import *
import numpy as np

__all__ = [
    'clip_radian_rotation', 'find_rotation', "theta_to_clock",
    'find_theta_distance', 'deg_to_theta'
]


def clip_radian_rotation(rad: float) -> float:
    """Clip the radian to be between (pi, pi] which is the common form in robotics.

    Parameters
    ----------
    rad : float
        The rotation given in radian. If beyond PI * 2, the additional revolutions are ignored.

    Returns
    -------
    float
        The clipped value between the range (-pi, pi]
    """

    while rad > np.pi:
        rad -= (np.pi*2)
    while rad <= -np.pi:
        rad += (np.pi*2)
    return rad


def deg_to_theta(deg: float) -> float:
    """Convert Degrees to Radian clipped between (-pi, pi]

    Parameters
    ----------
    deg : float
        Degrees

    Returns
    -------
    float
        Clipped radian
    """

    rad = np.deg2rad(deg)
    return clip_radian_rotation(rad)


def theta_to_clock(rad: float) -> int:
    """Map radian onto a clock (1-12), where theta = 0 is 12 o'clock and theta = np.pi/2 is 9'o clock

    Parameters
    ----------
    rad : float
        Theta, will be clipped to (-np.pi, np.pi] if outside of range.

    Returns
    -------
    int
        The hour hand of the clock
    """

    rad = clip_radian_rotation(rad)
    clock_hand = -(rad/0.523599)
    if clock_hand <= 0:
        clock_hand += 12
    if clock_hand > 12:
        clock_hand -= 12
    clock_hand = np.rint(clock_hand)
    return int(clock_hand.item(0))


def find_theta_distance(t1: float, t2: float) -> float:
    """Find the shortest theta that moves t1 to t2.

    Parameters
    ----------
    t1 : float
        theta 1
    t2 : float
        theta 2

    Returns
    -------
    float
        The theta [-np.pi, np.pi] that moves t1 to t2 

    """

    # make sure they are in valid range
    t1 = clip_radian_rotation(t1)
    t2 = clip_radian_rotation(t2)

    if t1 > 0 and t2 < 0:
        # through zero
        dist1 = np.abs(t2) + t1
        # through the other side
        dist2 = (np.pi + t2) + (np.pi - t1)
        if dist1 < dist2:
            val = dist1
        else:
            val = dist2 * 1
    elif t1 < 0 and t2 > 0:
        # through zero
        dist1 = np.abs(t1) + t2
        # through the other side
        dist2 = (np.pi + t1) + (np.pi - t2)
        if dist1 < dist2:
            val = dist1 * -1
        else:
            val = dist2
    else:
        # they are on the same side
        val = t2 - t1
    return val


def find_rotation(v1, v2):
    """
    Find the shortest rotation, theta (in radian) that will rotate v1 to v2

    parameters
    ----------
    v1 : numpy array
        2D array of the starting position
    v2 : numpy array
        2D array of the ending position

    returns
    -------
    float
        The rotation in radian that rotates v1 to v2

    """
    # calculate
    rot = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    return clip_radian_rotation(rot)

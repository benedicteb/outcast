import numpy as np


def  dir2angle(direction):
    """Takes a direction vector, f.ex. [-1,0] as input and
    returns a facing code, f.ex 2.
    """
    angle = int(round(np.arctan2(-direction[1], direction[0]) / np.pi * 2))
    return angle


def  angle2dir(angle):
    """Takes a facing code, f.ex. 2 as input and
    returns a direction vector, f.ex. [-1,0].
    """
    x = np.cos(angle * np.pi / 2)
    y = np.sin(angle * np.pi / 2)
    return np.array([x, y])

"""
Contains generic methods that might be used by several different modules.
Is not intended to contain any classes.
Reccomended to be imported like this: 'import Functions as func'
Then do, f.ex. func.vec2angle([-1,0])
"""

import numpy as np


def  vec2angle(vec):
    """Takes a direction vector, f.ex. [-1,0] as input and
    returns a facing code, f.ex 2.
    """
    angle = int(round(np.arctan2(-vec[1], vec[0]) / np.pi * 2))
    return angle


def  angle2vec(angle):
    """Takes a facing code, f.ex. 2 as input and
    returns a direction vector, f.ex. [-1,0].
    """
    x =  np.cos(angle * np.pi / 2)
    y = -np.sin(angle * np.pi / 2)  # Negatice becaue map is "upside down".
    return np.array([x, y])

#!/usr/bin/env python
"""
Contains placeable classes.
Things that goes on top of the landscape.
"""
class Placeable(object):
    """
    Base class for Persons and Items.
    """
    def __init__(self, position:
        if not isinstance(position, (tuple, list, np.ndarray)):
            logging.error(
                "Position should be arraylike with [x, y]. Set it to [0, 0]."
            )
            position = [0, 0]
        self.position = np.array(position)

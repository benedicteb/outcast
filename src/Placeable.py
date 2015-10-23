#!/usr/bin/env python
"""
Contains placeable classes.
Things that goes on top of the landscape.
"""

import numpy as np

class Placeable(object):
    """
    Base class for Persons and Items.
    """

    def __init__(self, position):
        """
        Defaults to facing north. Facing codes:
        - 0: North
        - 1: East
        - 2: South
        - 3: West
        """
        if not isinstance(position, (tuple, list, np.ndarray)):
            logging.error(
                "Position should be arraylike with [x, y]. Set it to [0, 0]."
            )
            position = [0, 0]
        self.position = np.array(position)
        self.facing = 0

    def get_sprite(self):
        # Rotate the sprite while keeping its center and size.
        # if self.thrust > 0:
            # rot_image = pygame.transform.rotate(
                # self.sprite_thrust, self.pitch*180/np.pi
            # )
        # else:
            # rot_image = pygame.transform.rotate(
                # self.sprite, self.pitch*180/np.pi
            # )
        # rot_rect = self.sprite.get_rect().copy()
        # rot_rect.center = rot_image.get_rect().center
        # rot_image = rot_image.subsurface(rot_rect).copy()
        return self.sprite

#!/usr/bin/env python
"""
Contains placeable classes.
Things that goes on top of the landscape.
"""
import numpy as np
import os
import pygame

import Game

class Placeable(object):
    """
    Base class for Persons and Items.
    """

    def __init__(self, position, sprite):
        """
        Defaults to facing north. Facing codes:
        - 0: North
        - 1: East
        - 2: South
        - 3: West

        @param sprite name of sprite-file, no need for path nor extension.
        """
        if not isinstance(position, (tuple, list, np.ndarray)):
            logging.error(
                "Position should be arraylike with [x, y]. Set it to [0, 0]."
            )
            position = [0, 0]

        self.position = np.array(position)
        self.facing = 0

        self.sprite = pygame.image.load(
            os.path.join(Game.Game.SPRITES_LOCATION, sprite) + Game.Game.SPRITES_EXT
        ).convert_alpha()

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

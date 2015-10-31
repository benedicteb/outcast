#!/usr/bin/env python
"""
Contains placeable classes.
Things that goes on top of the landscape.
"""
import numpy as np
import os
import pygame
import logging

import Game

class Placeable(object):
    """
    Base class for Persons and Items.
    """

    def __init__(self, position, sprite):
        """
        Defaults to facing south. Facing codes:
        - 0: South
        - 1: East
        - 2: North
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

        self._sprite = pygame.image.load(Game.resource_path(
            Game.Game.SPRITES_LOCATION, sprite + Game.Game.SPRITES_EXT
        )).convert_alpha()

    def get_sprite(self):
        # Rotate the sprite while keeping its center and size.
        rot_image = pygame.transform.rotate(
            self._sprite, self.facing*90
        )
        rot_rect = self._sprite.get_rect().copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

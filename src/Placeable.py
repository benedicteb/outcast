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
import Functions as func

class Placeable(object):
    """
    Base class for Persons and Items.
    """

    def __init__(self, position=None, sprite=None, game=None, world=None):
        """
        Defaults to facing south. Facing codes:
        - 0: East
        - 1: North
        - 2: West
        - 3: South

        @param sprite name of sprite-file, no need for path nor extension.
        """
        if not isinstance(position, (tuple, list, np.ndarray, type(None))):
            logging.error(
                "Position should be arraylike with [x, y]. Set it to None."
            )
            position = None

        self.position = np.array(position)
        self.facing = 3
        self.game = game
        self.world = world
        if not position is None:
            world.pointers[tuple(position)] = self

        self._sprite = pygame.image.load(Game.resource_path(
            Game.Game.SPRITES_LOCATION, sprite + Game.Game.SPRITES_EXT
        )).convert_alpha()
        self._sprite = pygame.transform.rotate(
            self._sprite, 90
        )

    def get_facing(self):
        """Directly returns this Placeables facing direction vector."""
        return func.angle2vec(self.facing)

    def get_target(self):
        """Directly returns coordinate of the square thos Placeable is facing."""
        return self.world.pointers[tuple(self.position + self.get_facing())]

    def get_sprite(self):
        # Rotate the sprite while keeping its center and size.
        rot_image = pygame.transform.rotate(
            self._sprite, self.facing*90
        )
        rot_rect = self._sprite.get_rect().copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

#!/usr/bin/env python

import os
import pygame

from Placeable import Placeable
import Game

"""
Contains item-related classes.
"""
class Item(Placeable):
    """
    Base class for all items.
    """
    def __init__(self, name, position):
        super(Item, self).__init__(position)

        self.name = name
        self.sprite = pygame.image.load(
            os.path.join(Game.Game.SPRITES_LOCATION, name.lower()) + Game.Game.SPRITES_EXT
        ).convert_alpha()

#!/usr/bin/env python
"""
Contains item-related classes.
"""
import os

class Item(object):
    """
    Base class for all items.
    """
    def __init__(self, name):
        self.name, self.sprite_filename = name, os.path.join(Game.SPRITES_LOCATION,
                name) + Game.SPRITES_EXT

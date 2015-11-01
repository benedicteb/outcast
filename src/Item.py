#!/usr/bin/env python

import os
import pygame

from Placeable import Placeable
import Game
from Text import TextDialog


"""
Contains item-related classes.
"""
class Item(Placeable):
    """
    Base class for all items.
    """
    def __init__(self, name, position, game=None, world=None):
        super(Item, self).__init__(position, name.lower(), game, world)
        self.name = name

    def interact(self):
        """
        Called when player interacts with this item.
        """
        TextDialog("It is a %s." % self.name, self.game)


class Page(Item):
    """
    Pages contain text.
    """
    def __init__(self, text, position, game=None, world=None):
        super(Page, self).__init__("Page", position, game, world)
        self.text = text

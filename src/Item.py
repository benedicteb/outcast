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
        super(Item, self).__init__(position, sprite=name.lower())
        self.name = name

class Page(Item):
    """
    Pages contain text.
    """
    def __init__(self, text, position):
        super(Page, self).__init__("Page", position)
        self.text = text

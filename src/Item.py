#!/usr/bin/env python

from Placeable import Placeable

"""
Contains item-related classes.
"""
class Item(Placeable):
    """
    Base class for all items.
    """
    def __init__(self, name, icon):
        super(Item, self).__init__(position)
        self.name, self.icon = name, icon

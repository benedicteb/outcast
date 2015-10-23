#!/usr/bin/env python
"""
Contains item-related classes.
"""
class Item(object):
    """
    Base class for all items.
    """
    def __init__(self, nam, icon):
        self.name, self.icon = name, icon

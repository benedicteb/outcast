#!/usr/bin/env python
"""
Contains player and NPC-classes.
"""
import logging

from Item import Item

class Person(object):
    """
    Base class for all characters in game.
    """
    DEFAULT_HEALTH = 100

    def __init__(self, health=DEFAULT_HEALTH, position):
        """
        Defaults to facing north. Facing codes:
        - 0: North
        - 1: East
        - 2: South
        - 3: West

        @param health The health that is given at init.
        @param position [x, y] the position at init.
        """
        if not isinstance(position, (tuple, list)):
            logging.error(
                "Position should be tuple/list with [x, y], set it to [0, 0]"
            )
            position = [0, 0]

        self.health, self.position, self.facing = health, position, 0

class Player(Person):
    """
    Contains the player-controlled character.
    """
    def __init__(self, health=DEFAULT_HEALTH, position):
        super(Player, self).__init__(health, position)

        self.inventory = []

    def give_item(self, item):
        if not isinstance(item, Item):
            logging.error(
                "Item given to player is not item instance."
            )
            return

        self.inventory.append(item)

class NPC(Person):
    """
    Contains a character controlled by the game.
    """
    def next_step():
        """
        Since the game controls this character, some algorithm should say where
        it moves.

        TODO
        """
        pass

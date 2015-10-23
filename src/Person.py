#!/usr/bin/env python
"""
Contains player and NPC-classes.
"""
import numpy as np
import pygame
import logging

from Item import Item

DEFAULT_HEALTH = 100

class Person(object):
    """
    Base class for all characters in game.
    """

    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        """
        Defaults to facing north. Facing codes:
        - 0: North
        - 1: East
        - 2: South
        - 3: West

        @param health The health that is given at init.
        @param position [x, y] the position at init.
        """
        if not isinstance(position, (tuple, list, np.ndarray)):
            logging.error(
                "Position should be tuple/list with [x, y], set it to [0, 0]"
            )
            position = [0, 0]

        self.health, self.position, self.facing = health, np.array(position), 0
        self.game, self.world = game, world


class Player(Person):
    """
    Contains the player-controlled character.
    """
    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        super(Player, self).__init__(position, game, world, health)

        self.inventory = []
        self.sprite = pygame.image.load('sprites/player.png').convert_alpha()
        self.move_cool = 0.25  # seconds
        self.move_time = np.inf
        self.velocity = np.array([0,0])

    def update(self):
        if (self.velocity != 0).any():
            newpos = self.position + self.velocity
            print self.world.board[tuple(newpos)]
            if self.world.board[tuple(newpos)] in ('g'):
                if self.move_time > self.move_cool:
                    self.position = newpos
                    self.move_time = 0
        self.move_time += self.game.dt

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

#!/usr/bin/env python
"""
Contains player and NPC-classes.
"""
import numpy as np
import pygame
import logging

from Placeable import Placeable
from Item import Item

DEFAULT_HEALTH = 100

class Person(Placeable):
    """
    Base class for all characters in game.
    """

    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        """
        @param health The health that is given at init.
        @param position [x, y] the position at init.
        """
        super(Person, self).__init__(position)
        self.health = health
        self.game = game
        self.world = world


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

            # Check if outside bounds of map
            inside_x = 0 <= newpos[0] < self.world.shape[0]
            inside_y = 0 <= newpos[1] < self.world.shape[1]

            # Check if new position is on walkable place
            on_walkable = self.world.board[tuple(newpos)] in ('g')

            # Only walk after certain cooldown
            cooldown_passed = self.move_time > self.move_cool

            # Check if step is valid, and if it is, move
            if (inside_x and inside_y and on_walkable and cooldown_passed):
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

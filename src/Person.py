#!/usr/bin/env python
"""
Contains player and NPC-classes.
"""
import os
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
    def __init__(self, position, game, world, sprite, health=DEFAULT_HEALTH):
        """
        @param health The health that is given at init.
        @param position [x, y] the position at init.
        """
        super(Person, self).__init__(position, sprite)
        self.health = health
        self.game = game
        self.world = world

        self.inventory = []
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

            # If new position is on water, must have boat
            if self.world.board[tuple(newpos)] == 'w':
                names = [item.name for item in self.inventory]
                has_boat = 'Boat' in names
                on_walkable = has_boat

            # Only walk after certain cooldown
            cooldown_passed = self.move_time > self.move_cool

            # Check if step is valid, and if it is, move
            if (inside_x and inside_y and on_walkable and cooldown_passed):
                self.position = newpos
                self.move_time = 0

        self.move_time += self.game.dt

    def speed_up(self, speed_vector):
        """
        Changes the velocity of the player.
        """
        self.velocity += speed_vector

class Player(Person):
    """
    Contains the player-controlled character.
    """
    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        super(Player, self).__init__(position, game, world, "player", health)

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
    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        super(NPC, self).__init__(position, game, world, "npc", health)

    def next_step(self):
        """
        Since the game controls this character, some algorithm should say where
        it moves.

        TODO
        """
        water_to_left = 0
        water_to_right = 0
        water_up = 0
        water_down = 0

        for i in range(self.position[0], self.world.shape[0]):
            water_to_right += 1

            if self.world.board[i, self.position[1]] == 'w':
                break

        for i in list(reversed(range(0, self.position[0]))):
            water_to_left += 1

            if self.world.board[i, self.position[1]] == 'w':
                break

        for i in range(self.position[1], self.world.shape[1]):
            water_up += 1

            if self.world.board[self.position[0], i] == 'w':
                break

        for i in list(reversed(range(0, self.position[1]))):
            water_down += 1

            if self.world.board[self.position[0], i] == 'w':
                break

        if np.random.random() > 0.8:
            right_direction = max([water_down, water_up, water_to_left,
                water_to_right])
            if right_direction == water_down:
                return np.asarray([0, -1])
            elif right_direction == water_up:
                return np.asarray([0, 1])
            elif right_direction == water_to_right:
                return np.asarray([1, 0])
            elif right_direction == water_to_left:
                return np.asarray([-1, 0])

        return np.asarray([0, 0])

    def update(self):
        """
        """
        goal = self.next_step()
        newpos = self.position + (self.velocity + goal)

        # If next is water, try turn
        is_water = self.world.board[tuple(newpos)] == 'w'
        if is_water:
            self.velocity = np.asarray([0, 0])

        # If at end of world, move
        at_yend = self.position[0] == (self.world.shape[0] - 1)
        at_xend = self.position[1] == (self.world.shape[1] - 1)
        if at_yend or at_xend:
            self.velocity = np.asarray([0, 0])

        if (self.velocity == [0, 0]).all():
            self.speed_up(goal)

        # Do the actual moving
        super(NPC, self).update()

    def interact():
        """
        Called when player interacts with this NPC.
        """
        pass

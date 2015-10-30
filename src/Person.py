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
from Text import TextDialog
from FindPath import Maze

DEFAULT_HEALTH = 100
DEFAULT_FEAR = 0
DEFAULT_HATE = 0

class Person(Placeable):
    """
    Base class for all characters in game.
    """

    persons = []
    players = []
    npcs = []

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
        self.move_cool = 0.10  # seconds
        self.move_time = np.inf
        self.velocity = np.array([0,0])
        self._add(self)

    @classmethod
    def _add(self, p):
        self.persons.append(p)

    def update(self):
        if len(self.game.text_dialog_queue) > 0:
            return
        if (self.velocity != 0).any():
            newpos = self.position + self.velocity
            self.move(newpos)
        self.move_time += self.game.dt

    def move(self, newpos):

        # Change facing direction
        change = newpos - self.position
        if change[1] > 0:
            self.facing = 0
        elif change[0] > 0:
            self.facing = 1
        elif change[1] < 0:
            self.facing = 2
        elif change[0] < 0:
            self.facing = 3

        # Check if outside bounds of map
        inside_x = 0 <= newpos[0] < self.world.shape[0]
        inside_y = 0 <= newpos[1] < self.world.shape[1]

        # Check if new position is on walkable place
        on_walkable = self.world.board[tuple(newpos)] in ('g')
        if on_walkable:
            for person in Person.persons + [self.game.player]:
                if person == self:
                    continue  # Cannot collide with self.
                if (newpos == person.position).all():
                    on_walkable = False

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
            return True
        else:
            return False

    def speed_up(self, speed_vector):
        """
        Changes the velocity of the player.
        """
        self.velocity += speed_vector

    def hurt(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self._die()

    def _die(self):
        self.dialog = "I died."
        self.update = self._update_dead

    def _update_dead(self):
        # Cannot do anything when dead.
        pass

    def give_item(self, item):
        if not isinstance(item, Item):
            logging.error(
                "Item given to player is not item instance."
            )
            return

        self.inventory.append(item)

class Player(Person):
    """
    Contains the player-controlled character.
    """
    def __init__(self, position, game, world, health=DEFAULT_HEALTH):
        super(Player, self).__init__(position, game, world, "player", health)
        self.interacting_with = None

    @classmethod
    def _add(self, p):
        self.players.append(p)
        self.persons.append(p)

    def give_item(self, item):
        """
        Player reads pages if they are picked up.
        """
        super(Player, self).give_item(item)

        TextDialog("You got %s!" % item.name.lower(), self.game)

        if item.name == "Page":
            TextDialog(item.text, self.game)

class NPC(Person):
    """
    Contains a character controlled by the game.
    """
    def __init__(self,
            position, game, world, health=DEFAULT_HEALTH,
            dialog=None, items=[],
            fear=DEFAULT_FEAR, hate=DEFAULT_HATE,
        ):
        super(NPC, self).__init__(position, game, world, "npc", health)
        self.dialog = dialog
        self.fear = fear
        self.hate = hate

        for item in items:
            self.give_item(item)
        self.set_target()
        self.set_path()

    @classmethod
    def _add(self, p):
        self.persons.append(p)
        self.npcs.append(p)

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

    def set_target(self):

        change = (self.position - self.game.player.position)
        if change.sum() <= 10 and max(self.fear, self.hate) > 50:
            if self.fear > self.hate:
                idealtarget = self.position + change
            else:
                idealtarget = self.position - change
        else:
            idealtarget = self.position + np.random.randint(-3, 3+1, size=2)

        for r in xrange(10):
            possibilities = []
            for x in xrange(-r, r+1):
                for y in xrange(-r, r+1):
                    target = idealtarget + [x, y]
                    inside_x = 0 <= target[0] < self.world.shape[0]
                    inside_y = 0 <= target[1] < self.world.shape[1]
                    if (inside_x and inside_y):
                        on_walkable = self.world.board[tuple(target)] in ('g')
                        if on_walkable:
                            possibilities.append(target)
            if not possibilities:
                continue
            else:
                self.target = possibilities[np.random.randint(0, len(possibilities))]
                break

    def set_path(self):
        maze = Maze(
            self.position,
            self.target,
            self.world.board == 'g',
        )
        self.path = maze.solve(10)

    def update(self, depth=0):
        """
        """

        if len(self.game.text_dialog_queue) > 0:
            return False

        # Only walk after certain cooldown
        cooldown_passed = self.move_time > self.move_cool
        if cooldown_passed:
            if not self.path:  # if empty or None
                self.set_target()
                self.set_path()
            if self.path:
                newpos = self.path[0]
                if self.move(newpos):  # Successfull move.
                    del self.path[0]
                elif depth >= 10:
                    # Move was blocked by some entity.
                    # Clear current path and try again.
                    # Maxium depth to avoid potential infinite recursive loop.
                    self.path = []
                    self.update(depth+1)
                    return
                else:
                    self.path = []
                self.move_time = 0
            else:  # Else backup solution.
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
                newpos = self.position + self.velocity
                super(NPC, self).move(newpos)

        self.move_time += self.game.dt

    def interact(self):
        """
        Called when player interacts with this NPC.
        """

        self.fear -= 50
        if not self.dialog:
            return

        TextDialog(self.dialog, self.game)
        self.dialog = "I have nothing more to tell you."

        for i in range(len(self.inventory)):
            self.game.player.give_item(self.inventory.pop(i))

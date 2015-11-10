#!/usr/bin/env python

# import os
# import pygame

from Placeable import Placeable
import Game
import Person
import Functions as func


SPEED_MOVE = 20.  # [meter/sec]


"""
Contains projectile-related classes.
"""
class Projectile(Placeable):
    """
    Projectiles, like fireballs, arrows.
    """
    def __init__(self, name, position, facing, game=None, world=None):
        super(Projectile, self).__init__(position, name.lower(), game, world)
        self.name = name
        self.game.projectiles.append(self)

        self.facing = facing
        self.cooldown_move = 1. / SPEED_MOVE  # seconds
        self.cooldown_time = 0.
        self.velocity = func.angle2vec(facing)


    def update(self):
        if len(self.game.text_dialog_queue) > 0:
            return
        newpos = self.position + self.velocity
        self.move(newpos)
        self.cooldown()


    def cooldown(self):
        self.cooldown_time -= self.game.dt
        if self.cooldown_time < 0:
            self.cooldown_time = 0
            self.action = "none"

    def is_cooldowned(self):
        if self.cooldown_time == 0:
            return True
        else:
            return False


    def move(self, newpos):

        # Check if outside bounds of map
        inside_x = 0 <= newpos[0] < self.world.shape[0]
        inside_y = 0 <= newpos[1] < self.world.shape[1]

        # Check if new position is on walkable place
        on_walkable = self.world.board[tuple(newpos)] in ('g', 'w')
        if on_walkable:
            p =  self.world.pointers[tuple(newpos)]
            if isinstance(p, Person.Person):
                # A Person is in the way.
                self.attack(p)

        # Check if step is valid, and if it is, move
        if (inside_x and inside_y and on_walkable and self.is_cooldowned()):
            self.world.pointers[tuple(self.position)] = None
            self.position = newpos
            self.world.pointers[tuple(self.position)] = self
            self.cooldown_time += self.cooldown_move
            return True
        else:
            return False


    def attack(self, p):
        """Hurt p, if p is a hurtable Person."""
        try:
            dmg = 100
            p.hurt(dmg)
        except AttributeError:  # Nothing to attack.
            pass

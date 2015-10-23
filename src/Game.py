import sys
import numpy as np
import pygame
from pygame.locals import *

from World import World
from Person import Player


class Game:


    def __init__(self):
        self.FPS = 30
        self.dt = 1. / self.FPS
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sight_radius = 10
        self.width  = (2*self.sight_radius + 1) * World.METER_SIZE
        self.height = (2*self.sight_radius + 1) * World.METER_SIZE
        self.screen = pygame.display.set_mode((
            self.width, self.height
        ))
        pygame.display.set_caption('Testing')
        self.world = World(open("worlds/firstworld.board", 'r'))
        self.world.game = self

        self.player = Player([0, 0], game=self, world=self.world)
        # self.world.add(self.player)
        # self.world.add(Planet([200,200], 500, 30))


    def start(self):
        self._draw()
        while 1:
            self._update()
            self._draw()
            self.dt = self.clock.tick(self.FPS) * 0.001
            # print self.clock.get_fps()


    def _update(self):

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_a, K_d, K_w, K_s):
                    if event.key == K_a:
                        self.player.velocity[0] -= 1
                    elif event.key == K_d:
                        self.player.velocity[0] += 1
                    elif event.key == K_w:
                        self.player.velocity[1] -= 1
                    elif event.key == K_s:
                        self.player.velocity[1] += 1
            elif event.type == KEYUP:
                if event.key in (K_a, K_d, K_w, K_s):
                    if event.key == K_a:
                        self.player.velocity[0] += 1
                    elif event.key == K_d:
                        self.player.velocity[0] -= 1
                    elif event.key == K_w:
                        self.player.velocity[1] += 1
                    elif event.key == K_s:
                        self.player.velocity[1] -= 1

        self.player.update()


    def _draw(self):

        board = self.world.board
        radius = self.sight_radius
        playpos = self.player.position

        self.screen.fill(World.VOID_COLOR)
        for i in xrange(-radius, radius + 1):
            for j in xrange(-radius, radius + 1):
                ij = np.array([i, j])
                try:
                    if (ij + playpos < 0).any():
                        raise IndexError
                    key = board[tuple(ij + playpos)]
                except IndexError:
                    # Outside of board.
                    continue
                self.screen.blit(
                    self.world.sprites[key],
                    (ij + radius) * World.METER_SIZE,
                )
        self.screen.blit(
            self.player.sprite,
            np.array([radius, radius]) * World.METER_SIZE,
        )
        pygame.display.update()


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

        self.player = Player([3, 3])
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
                if event.key == K_LEFT or event.key == K_a:
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
                    pass
                elif event.key == K_UP or event.key == K_w:
                    pass
                elif event.key == K_DOWN or event.key == K_s:
                    pass
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
                    pass
                elif event.key == K_UP or event.key == K_w:
                    pass
                elif event.key == K_DOWN or event.key == K_s:
                    pass


    def _draw(self):

        board = self.world.board
        radius = self.sight_radius
        playpos = self.player.position

        self.screen.fill(World.VOID_COLOR)
        for i, columns in enumerate(board[playpos[0]-radius : playpos[0]+radius+1]):
            # print i
            for j, square in enumerate(columns[playpos[1]-radius : playpos[1]+radius+1]):
                self.screen.blit(
                    self.world.sprites[board[i,j]],
                    (i * World.METER_SIZE, j* World.METER_SIZE),
                )
        self.screen.blit(
            self.player.sprite,
            playpos * World.METER_SIZE,
        )
        pygame.display.update()


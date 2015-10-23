import sys
import numpy as np
import pygame
from pygame.locals import *

from World import World


class Game:


    def __init__(self):
        self.FPS = 30
        self.dt = 1. / self.FPS
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sight_radius = 20
        self.width  = 41 * World.METER_SIZE
        self.height = 41 * World.METER_SIZE
        self.screen = pygame.display.set_mode((
            self.width, self.height
        ))
        pygame.display.set_caption('Testing')
        self.world = World(open("worlds/firstworld.board", 'r'))
        self.world.game = self

        self.playerpos = np.array([3, 3])
        # self.player = Plane(pos=[200,20], velocity=[33,0])
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

        self.screen.fill(World.VOID_COLOR)
        for i, row in enumerate(board[self.playerpos[0]-radius : self.playerpos[0]+radius+1]):
            # print i
            for j, square in enumerate(row[self.playerpos[1]-radius : self.playerpos[1]+radius+1]):
                self.screen.blit(
                    self.world.sprites[board[i,j]],
                    (j * World.METER_SIZE, i* World.METER_SIZE),
                )
        # self.screen.blit(
            # self.player.get_sprite(),
            # player_sprite_pos+offset,
        # )
        pygame.display.update()


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
        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode((
            self.width, self.height
        ))
        pygame.display.set_caption('Testing')
        self.world = World()
        self.world.game = self
        # self.player = Plane(pos=[200,20], velocity=[33,0])
        # self.world.add(self.player)
        # self.world.add(Planet([200,200], 500, 30))


    def start(self):
        self._draw()
        while 1:
            self._update()
            self._draw()
            self.dt = self.clock.tick(self.FPS) * 0.001
            print self.clock.get_fps()


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
        # self.screen.blit(
            # self.player.get_sprite(),
            # player_sprite_pos+offset,
        # )
        pygame.display.update()


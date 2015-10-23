import numpy as np
import pygame


class World:

    METER_SIZE = 20  # Number of pixels per square side.
    VOID_COLOR = (0, 0, 0)


    def __init__(self, infile=None, void_color=VOID_COLOR):

        if not infile is None:
            board = []
            for line in infile:
                board.append(list(line.strip()))
            self.board = np.array(board).transpose()
            self.shape = self.board.shape
        self.void_color = void_color
        self.game = None

        self.sprites = {
            'g': pygame.image.load('sprites/grass.png').convert(),
            'w': pygame.image.load('sprites/water.png').convert(),
        }


    def add(self, thing):
        pass

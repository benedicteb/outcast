import os
import numpy as np
import pygame

import Game


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
        else:
            board = real_world.split()
            for i, line in enumerate(board):
                board[i] = list(line.strip())
            self.board = np.array(board).transpose()
            self.shape = self.board.shape

        self.void_color = void_color
        self.game = None

        self.sprites = {
            'g': pygame.image.load(
                Game.resource_path(os.path.join(
					Game.Game.SPRITES_LOCATION, 'grass.png'))
            ).convert(),
            'w': pygame.image.load(
                Game.resource_path(os.path.join(
					Game.Game.SPRITES_LOCATION, 'water.png'))
            ).convert(),
            't': pygame.image.load(
                Game.resource_path(os.path.join(
					Game.Game.SPRITES_LOCATION, 'tree.png'))
            ).convert(),
        }


    def add(self, thing):
        pass

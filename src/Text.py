#! /usr/bin/env python
"""
Contains class for displaying text on the screen.
"""
import os
import pygame

import Game

class TextDialog(object):
    """
    """
    COLOR = (0, 0, 0)
    MARGIN = 20

    def __init__(self, text, game):
        self.text = text
        self.game = game

        self.bg_sprite = pygame.image.load(
            os.path.join(Game.Game.SPRITES_LOCATION, "text_prompt") + Game.Game.SPRITES_EXT
        ).convert_alpha()

        self.x = (game.width - Game.Game.STATUSBAR_OFFSET)/2
        self.y = game.height - 10 - self.bg_sprite.get_height()

        self.printed_to = 0

        self.font = pygame.font.Font(Game.Game.CANTERBURY_FONT, 12)

        self.finished = 0

        # Get first page
        self.next_page()

        self.game.text_dialog_queue.append(self)

    def next_page(self):
        """
        Renders the next page of text. If None is returned there is no more text
        and the dialog is removed.
        """
        self.line1, self.line2 = self._get_objects(self.printed_to)

        if self.printed_to == len(self.text):
            self.finished += 1

        if self.finished == 2:
            return False
        else:
            return True

    def render(self):
        """
        """
        self.game.screen.blit(self.bg_sprite, [self.x, self.y])

        x = self.x + self.MARGIN
        y = self.y + self.MARGIN

        self.game.screen.blit(self.line1, [x, y])

        y += self.line1.get_height() + 5

        if self.line2:
            self.game.screen.blit(self.line2, [x, y])

        if self.printed_to != len(self.text):
            label = self.font.render(">", 1, self.COLOR)
            self.game.screen.blit(label, [x, y + self.line2.get_height()])

    def _get_objects(self, start):
        """
        """
        line1 = self.font.render(self.text[self.printed_to:], 1, self.COLOR)
        i = len(self.text)

        while line1.get_width() > self.bg_sprite.get_width() - 2*self.MARGIN:
            line1 = self.font.render(self.text[self.printed_to:i], 1, self.COLOR)
            i -= 1

        self.printed_to = i

        # If there is text left
        if self.printed_to != len(self.text):
            line2 = self.font.render(self.text[self.printed_to:], 1, self.COLOR)
            i = len(self.text)

            while line2.get_width() > self.bg_sprite.get_width() - 2*self.MARGIN:
                line2 = self.font.render(self.text[self.printed_to:i], 1, self.COLOR)
                i -= 1

            self.printed_to = i
        else:
            line2 = None

        return line1, line2

import sys
import os
import numpy as np
import pygame
from pygame.locals import *

from World import World
from Person import Player, NPC
from Item import Item, Page
from Text import TextDialog

# Just some dummy text
PAGE1="""A long time ago, in a galaxy far far away. There once was a princess
called Rapunzel. She had been bewitched by an evil wizard."""
PAGE2="""When she grew up she wanted to be rid of the curse. However even though
the king summoned every wizard and witch in the kingdom, none could dissolve the
curse."""
PAGE3="""Then one day a beautiful prince approached the king. He told him that
he had learned from a fairy how to bewitchment could be dissolved. He just had
to build a ship that could fly, swim and also run on land."""
PAGE4="""The king said: Building this vehicle would require a thousand men and
excellent leadership. If they were going to pull that off he would need the help
of the prince. As well as the rest of the kingdom."""

class Game:
    SPRITES_LOCATION = "sprites/"
    SPRITES_EXT = ".png"

    CANTERBURY_FONT = os.path.join("fonts", "Canterbury.ttf")
    MONOSPACE_FONT = os.path.join("fonts", "Monospace.ttf")

    STATUSBAR_OFFSET = 120
    STATUSBAR_COLOR = (112, 112, 112)
    STATUSBAR_FONTSIZE = 24
    STATUSBAR_MARGIN = 10

    # Inventory
    INV_OFF = 10
    INV_SPACE = 5
    INV_WIDTH = 20
    INV_HEIGHT = 20
    INV_ROWS = 4
    INV_COLS = 4

    def __init__(self):
        self.FPS = 30
        self.dt = 1. / self.FPS
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sight_radius = 10
        self.width  = (2*self.sight_radius + 1) * World.METER_SIZE + Game.STATUSBAR_OFFSET
        self.height = (2*self.sight_radius + 1) * World.METER_SIZE
        self.screen = pygame.display.set_mode((
            self.width, self.height
        ))
        pygame.display.set_caption('Testing')
        self.world = World(open("worlds/real_world.board", 'r'))
        self.world.game = self

        self.player = Player([11, 11], game=self, world=self.world)
        # self.world.add(self.player)
        # self.world.add(Planet([200,200], 500, 30))

        self.placables = [
            # Item("Axe", position=[10, 3]),
            # Item("Boat", position=[2, 3]),
            Page(PAGE1, position=[72, 13]),
            # Page(PAGE2, position=[21, 3]),
            # Page(PAGE3, position=[22, 3]),
        ]

        self.npcs = [
            # NPC([0, 1], game=self, world=self.world, dialog="This is a page. Cherish it well!",
            #     items=[Page(PAGE4, position=None)]),
            # NPC([0, 2], game=self, world=self.world, dialog="My my, this is fancy!"),
        ]

        self.text_dialog_queue = []

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
                if event.key in (K_a, K_d, K_w, K_s) and not len(self.text_dialog_queue) != 0:
                    if event.key == K_a:
                        self.player.speed_up([-1, 0])
                    elif event.key == K_d:
                        self.player.speed_up([1, 0])
                    elif event.key == K_w:
                        self.player.speed_up([0, -1])
                    elif event.key == K_s:
                        self.player.speed_up([0, 1])
                if event.key == K_e:
                    if len(self.text_dialog_queue) != 0:
                        if not self.text_dialog_queue[0].next_page():
                            del self.text_dialog_queue[0]

                            if self.player.interacting_with and len(self.text_dialog_queue) == 0:
                                self.player.interacting_with = None
                                continue

                    for npc in self.npcs:
                        for ds in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                            if (npc.position == self.player.position + ds).all():
                                if not self.player.interacting_with and not len(self.text_dialog_queue) != 0:
                                    npc.interact()
                                    self.player.interacting_with = npc

            elif event.type == KEYUP:
                if event.key in (K_a, K_d, K_w, K_s) and not len(self.text_dialog_queue) != 0:
                    if event.key == K_a:
                        self.player.speed_up([1, 0])
                    elif event.key == K_d:
                        self.player.speed_up([-1, 0])
                    elif event.key == K_w:
                        self.player.speed_up([0, 1])
                    elif event.key == K_s:
                        self.player.speed_up([0, -1])

        # If player steps on item, give it to player
        for item in self.placables:
            if (self.player.position == item.position).all():
                self.player.give_item(self.placables.pop(self.placables.index(item)))

        self.player.update()

        for npc in self.npcs:
            npc.update()

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
                    (ij + radius) * World.METER_SIZE + [Game.STATUSBAR_OFFSET, 0],
                )


        self.screen.blit(
            self.player.sprite,
            np.array([radius, radius]) * World.METER_SIZE + [Game.STATUSBAR_OFFSET, 0],
        )

        # Draw statusbar
        pygame.draw.rect(self.screen, Game.STATUSBAR_COLOR, (0, 0,
            Game.STATUSBAR_OFFSET, self.height), 0)

        # Text for statusbar
        font = pygame.font.Font(Game.CANTERBURY_FONT, Game.STATUSBAR_FONTSIZE)
        label = font.render("Inventory", 1, (0, 0, 0))
        self.screen.blit(label, (Game.STATUSBAR_MARGIN, Game.STATUSBAR_MARGIN))

        # Draw inventory boxes
        for i in range(Game.INV_COLS):
            for j in range(Game.INV_ROWS):
                pygame.draw.rect(self.screen, (0,0,0), (Game.INV_WIDTH*i +\
                    Game.INV_OFF + Game.INV_SPACE*i, Game.STATUSBAR_MARGIN +\
                    label.get_height() + Game.INV_OFF + Game.INV_HEIGHT*j +\
                    Game.INV_SPACE*j, Game.INV_WIDTH,
                    Game.INV_HEIGHT), 0)

        # If player has inventory, fill
        for i in range(len(self.player.inventory)):
            x = i % Game.INV_COLS
            y = i / Game.INV_ROWS

            self.screen.blit(
                    self.player.inventory[i].get_sprite(),
                    [Game.INV_OFF + Game.INV_SPACE*x + Game.INV_WIDTH*x,
                     Game.STATUSBAR_MARGIN + label.get_height() + Game.INV_OFF +\
                     Game.INV_HEIGHT*y + Game.INV_SPACE*y])

        # Draw FPS
        FPS = 1. / self.dt
        font = pygame.font.Font(Game.MONOSPACE_FONT, Game.STATUSBAR_FONTSIZE)
        label = font.render("FPS: %d" % FPS, 1, (255, 0, 0))
        self.screen.blit(label, (self.width - label.get_width(), 0))

        # Draw placables
        for item in self.placables:
            self.screen.blit(item.get_sprite(),
                    (item.position - self.player.position + radius) * World.METER_SIZE +\
                    [Game.STATUSBAR_OFFSET, 0])

        # Draw NPCs
        for npc in self.npcs:
            self.screen.blit(npc.get_sprite(),
                    (npc.position - self.player.position + radius) * World.METER_SIZE +\
                    [Game.STATUSBAR_OFFSET, 0])

        # If text dialog, draw it
        if len(self.text_dialog_queue) != 0:
            self.text_dialog_queue[0].render()

        pygame.display.update()

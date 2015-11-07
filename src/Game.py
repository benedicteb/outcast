import sys
import os
import numpy as np
import pygame
from pygame.locals import *

from World import World
from Person import Player, NPC
from Item import Item, Page
from Text import TextDialog
import Functions as func

PAGE1="""Page 1:
The others stay away from me. I am no longer welcome anywhere. Even
though what I did was horrible, the punishment feels much, much worse. Don't
they realise that I grieve as well?"""

PAGE2="""Page 2:
The plains are green, everything is green. Except the ocean
surrounding our island. It hasn't always been like this. It's my fault, why
wasn't I more careful?"""

PAGE3="""Page 3:
Once this island housed a huge city. Technology was everywhere. The
kingdom was filled with prosperity and everyone were kind to each other. The
trouble started when an ancient burial ground revealed a giant underground cave
system."""

PAGE4="""Page 4:
With our technology we delved, we delved deep and deep into the caves. Where the
caves stopped, we found an altar. The altar had a scroll of text. Both the altar
and the scroll was brought to the surface."""

PAGE5="""Page 5:
I was part of the team of scientists tasked with decrypting the scroll. It was
some remnant of an ancient civilization living here before us. The decrypting
took a long time."""

PAGE6="""Page 6.
At last, we did it. The scroll told of magic. It had complex diagrams and
formulas. Diagrams showing how to wave your arms, and text describing how to
pronounce incantations. Most of us thought it to be superstition."""

PAGE7="""Page 7:
The magic works! Just for fun I tried some of the instructions the
scroll told of. Suddenly a fireball erupted from my hand. The research academy
burned down."""

PAGE8="""Page 8:
People are worried. The news has spread for some time now. Everyone wants to
hide this scroll, back where it was found. I'm trying to convince to don't.
Imagine the wonders this can do for our civilization. We can be even greater
than we already are!"""

PAGE9="""Page 9:
In my folly I continued to play with fireballs. Today I hit the town
cathedral - the biggest tribute to our civilization! It burned down, everything
burnt down.  The fire spread so fast, it is not natural. They have abandoned me
now, on the outskirts of town. I am never to show my face again. I have ruined
everything."""

def resource_path(*pathnames):
    relative_path = pathnames[0]
    for pname in pathnames[1:]:
        relative_path = os.path.join(relative_path, pname)
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Game:
    SPRITES_LOCATION = "sprites"
    SPRITES_EXT = ".png"

    FONTS_LOCATION = "fonts"
    CANTERBURY_FONT = "Canterbury.ttf"
    MONOSPACE_FONT = "Monospace.ttf"

    WORLDS_LOCATION = "worlds"

    STATUSBAR_OFFSET = 120
    STATUSBAR_COLOR = (112, 112, 112)
    STATUSBAR_FONTSIZE = 24
    STATUSBAR_MARGIN = 10

    # Inventory
    INV_OFF = 10
    INV_SPACE = 5
    INV_WIDTH = 20
    INV_HEIGHT = 20
    INV_ROWS = 15
    INV_COLS = 4

    keymap = {
        K_d : func.angle2vec(0),
        K_w : func.angle2vec(1),
        K_a : func.angle2vec(2),
        K_s : func.angle2vec(3),
        K_RIGHT : func.angle2vec(0),
        K_UP    : func.angle2vec(1),
        K_LEFT  : func.angle2vec(2),
        K_DOWN  : func.angle2vec(3),
    }

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
        self.world = World(open(resource_path(
            Game.WORLDS_LOCATION, "real_world.board"
        ), 'r'))
        self.world.game = self

        self.player = Player([11, 11], game=self, world=self.world)

        self.placables = [
            Item("Axe", position=[53, 16], game=self, world=self.world),
            Item("Boat",position=[14, 63], game=self, world=self.world),
            Page(PAGE1, position=[19, 11], game=self, world=self.world),
            Page(PAGE2, position=[26, 16], game=self, world=self.world),
            Page(PAGE3, position=[61, 12], game=self, world=self.world),
        ]

        self.npcs = [
            NPC([72, 58], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE4, position=None)]),
            NPC([34, 74], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE5, position=None)]),
            NPC([63, 84], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE6, position=None)]),
            NPC([25, 32], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE7, position=None)]),
            NPC([57, 37], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE8, position=None)]),
            NPC([31, 51], game=self, world=self.world, dialog="This is a page. Maybe you'll learn something, douche.",
                items=[Page(PAGE9, position=None)]),
        ]

        self.text_dialog_queue = []

    def start(self):
        self._draw_init()
        self._draw_inventory()
        self._draw()
        while 1:
            self._update()
            self._draw()
            self.dt = self.clock.tick(self.FPS) * 0.001


    def _update(self):
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in Game.keymap.keys():
                    self.player.speed_up(Game.keymap[event.key])
                elif event.key == K_e:
                    if len(self.text_dialog_queue) > 0:
                        if not self.text_dialog_queue[0].next_page():
                            del self.text_dialog_queue[0]

                            if self.player.interacting_with and len(self.text_dialog_queue) == 0:
                                self.player.interacting_with = None
                                continue
                    else:
                        try:
                            self.player.get_target().interact()
                        except AttributeError:
                            pass  # Nothing to interact with.

            elif event.type == KEYUP:
                if event.key in Game.keymap.keys():
                    self.player.speed_up(- Game.keymap[event.key])

        # If player steps on item, give it to player
        for item in self.placables:
            if (self.player.position == item.position).all():
                self.player.give_item(self.placables.pop(self.placables.index(item)))
                self._draw_inventory()

        self.player.update()
        for npc in self.npcs:
            npc.update()


    def _draw(self):
        board = self.world.board
        radius = self.sight_radius
        playpos = self.player.position

        for i in xrange(-radius, radius + 1):
            for j in xrange(-radius, radius + 1):
                ij = np.array([i, j])

                try:
                    if (ij + playpos < 0).any():
                        raise IndexError
                    key = board[tuple(ij + playpos)]
                except IndexError:
                    key = 'v'  # outside of board => void

                # Draw terrain
                self.screen.blit(
                    self.world.sprites[key],
                    (ij + radius) * World.METER_SIZE + [Game.STATUSBAR_OFFSET, 0],
                )
                if key == 'v':
                    continue   # No placeables in void.

                # Draw placeables
                if not self.world.pointers[tuple(ij + playpos)] is None:
                    self.screen.blit(
                        self.world.pointers[tuple(ij + playpos)].get_sprite(),
                        (ij + radius) * World.METER_SIZE +
                        [Game.STATUSBAR_OFFSET, 0],
                    )

        # Draw FPS
        FPS = 1. / self.dt
        font = pygame.font.Font(
            # Game.MONOSPACE_FONT,
            resource_path(Game.FONTS_LOCATION, Game.MONOSPACE_FONT),
            Game.STATUSBAR_FONTSIZE,
        )

        # If text dialog, draw it
        if len(self.text_dialog_queue) != 0:
            self.text_dialog_queue[0].render()

        pygame.display.update()


    def _draw_inventory(self):

        # Draw inventory boxes
        for i in range(Game.INV_COLS):
            for j in range(Game.INV_ROWS):
                pygame.draw.rect(self.screen, (0,0,0), (Game.INV_WIDTH*i +\
                    Game.INV_OFF + Game.INV_SPACE*i, Game.STATUSBAR_MARGIN +\
                    Game.STATUSBAR_LABEL_HEIGHT +
                        Game.INV_OFF + Game.INV_HEIGHT*j +\
                    Game.INV_SPACE*j, Game.INV_WIDTH,
                    Game.INV_HEIGHT), 0)

        # If player has inventory, fill
        for i in range(len(self.player.inventory)):
            x = i % Game.INV_COLS
            y = i / Game.INV_ROWS
            self.screen.blit(
                    self.player.inventory[i].get_sprite(),
                    [Game.INV_OFF + Game.INV_SPACE*x + Game.INV_WIDTH*x,
                     Game.STATUSBAR_MARGIN + Game.STATUSBAR_LABEL_HEIGHT +
                        Game.INV_OFF +\
                     Game.INV_HEIGHT*y + Game.INV_SPACE*y])


    def _draw_init(self):

        # Draw statusbar
        pygame.draw.rect(self.screen, Game.STATUSBAR_COLOR, (0, 0,
            Game.STATUSBAR_OFFSET, self.height), 0)

        # Text for statusbar
        font = pygame.font.Font(
            resource_path(Game.FONTS_LOCATION, Game.CANTERBURY_FONT),
            Game.STATUSBAR_FONTSIZE,
        )
        label = font.render("Inventory", 1, (0, 0, 0))
        Game.STATUSBAR_LABEL_HEIGHT = label.get_height()
        self.screen.blit(label, (Game.STATUSBAR_MARGIN, Game.STATUSBAR_MARGIN))

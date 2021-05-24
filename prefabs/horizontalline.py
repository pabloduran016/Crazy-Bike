from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
from settings.FLOORS import *
import settings.FLOORS as FLOORS
import pygame
import pygame.gfxdraw
from functions import scale


class HorizontalLine(Floor):
    def __init__(self, game, position, length, width):
        """
        :type game: main.Game
        :type position: Vec2d
        :type length: float
        :type width: int
        """
        shape = Segment(body=None, a=(0, 0), b=(length, 0), radius=RADIUS)
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.length = length
        self.width = width
        self.fill = FILL
        self.lastpoint = Vec(length, 0) + position
        self.vertices = [Vec(0, 20), Vec(length, 20), Vec(length, width), Vec(0, width)]
        self.grass = [Vec(0, 0), Vec(length, 0), Vec(length, 20), Vec(0, 20)]
        self.slope = 0
        self.eq = lambda x: 0

    def draw(self):
        offset = self.body.position*self.game.zoom - self.game.camera
        for group, tex in ((self.vertices, 'ground'), (self.grass, 'grass')):
            points = [(p + self.body.position) * self.game.zoom - self.game.camera + self.game.displacement
                      for p in group]
            try:
                pygame.gfxdraw.textured_polygon(self.game.screen, points,
                                                scale(self.game.textures[tex], zoom=self.game.zoom),
                                                round(offset.x), -round(offset.y))
            except pygame.error:
                pass

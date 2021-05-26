from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
from settings.FLOORS import *
import settings.FLOORS as FLOORS
import pygame
import pygame.gfxdraw
from functions import scale


class Line(Floor):
    def __init__(self, game, position, final_pos, width):
        """
        :type game: main.Game
        :type position: Vec2d
        :type final_pos: Vec2d
        :type width: int
        """
        shape = Segment(body=None, a=(0, 0), b=final_pos-position, radius=RADIUS)
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.width = width
        self.length = (final_pos - position).x
        self.height = (final_pos - position).y
        self.fill = FILL
        self.lastpoint = Vec(final_pos[0], final_pos[1])
        self.vertices = [Vec(0, 0), self.lastpoint - position, self.lastpoint - position + Vec(0, self.width),
                         Vec(0, self.width)]
        self.grass = [Vec(0, 0), self.lastpoint - position, self.lastpoint - position + Vec(0, 20),
                         Vec(0, 20)]
        self.slope = self.height/self.length
        self.eq = lambda p: self.slope*p

    def draw(self):
        offset = self.body.position*self.game.zoom - self.game.camera + self.game.displacement
        for group, tex in ((self.vertices, 'ground'), (self.grass, 'grass')):
            points = [(p + self.body.position) * self.game.zoom - self.game.camera + self.game.displacement
                      for p in group]
            try:
                pygame.gfxdraw.textured_polygon(self.game.screen, points,
                                                scale(self.game.textures[tex], zoom=self.game.zoom),
                                                round(offset.x), -round(offset.y))
            except pygame.error:
                pass

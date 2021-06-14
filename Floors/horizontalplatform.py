from .floor_baseclass import Floor
from pymunk import Poly
from settings.FLOORS import *
import settings.FLOORS as FLOORS
import pygame


class HorizontalPlatform(Floor):
    def __init__(self, position, length, width, **kwargs):
        """
        :type position: pymunk.Vec2d
        """
        self.vertices = [(0, 0), (length, 0), (length, width), (0, width)]
        shape = Poly(body=None, vertices=self.vertices, radius=RADIUS)
        self.width = width
        self.fill = FILL
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.lastpoint = (length, 0) + self.body.position
        self.length = length
        self.eq = lambda x: 0

    def draw(self):
        vertices = [vertice + self.body.position - self.game.camera.position for vertice in self.vertices]
        pygame.draw.polygon(self.game.screen, self.color, vertices, self.fill)
        # pygame.draw.lines(self.game.screen, self.color, closed=True, points=vertices, width=4)
        pass

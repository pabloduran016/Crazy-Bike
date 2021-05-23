from .floor_baseclass import Floor
from math import cos, sin
from pymunk import Vec2d as Vec
from pymunk import Poly
from settings.FLOORS import *
import settings.FLOORS as FLOORS
import pygame


class Platform(Floor):
    def __init__(self, game, position, angle, length, width):
        """
        :type game: main.Game
        :type position: pymunk.Vec2d
        """
        self.vertices = [(0, 0), length * Vec(cos(angle), -sin(angle)), Vec(cos(angle) * length,
                         length * (-sin(angle)) + width), (0, width)]
        shape = Poly(body=None, vertices=self.vertices, radius=RADIUS)
        self.width = width
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.length = length
        self.height = -sin(angle)*length
        self.lastpoint = Vec(cos(angle), -sin(angle)) * length + self.body.position
        self.slope = self.length/self.height
        self.eq = lambda x: self.slope*x

    def draw(self):
        vertices = [vertice + self.body.position - self.game.camera for vertice in self.vertices]
        pygame.draw.polygon(self.game.screen, self.color, vertices, self.width)
        # pygame.draw.lines(self.game.screen, self.color, closed=True, points=vertices, width=4)

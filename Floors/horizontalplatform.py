from .floor_baseclass import Floor
from pymunk import Poly
from pymunk import Vec2d as Vec
from settings.FLOORS import *
import settings.FLOORS as FLOORS
import pygame
from typing import Union, Tuple


class HorizontalPlatform(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], length: float, width: float, **kwargs):
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

    def draw(self) -> None:
        vertices = [vertice + self.body.position - self.game.camera.position for vertice in self.vertices]
        pygame.draw.polygon(self.game.screen, self.color, vertices, self.fill)
        # pygame.draw.lines(self.game.screen, self.color, closed=True, points=ground, width=4)
        pass

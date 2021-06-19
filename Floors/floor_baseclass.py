import pymunk
from pymunk import Vec2d, Body as Vec, Body
from settings.FLOORS import *
from abc import ABC, abstractmethod
import pygame
import pygame.gfxdraw
from Utilities import scale
from typing import List, Union, Tuple
# from game import Physics


class Floor(ABC):
    def __init__(self, game, physics, position: Union[Vec, Tuple[float, float]], subclass,
                 shape: Union[List[pymunk.Shape], pymunk.Shape]):
        """
        :type game: game.Game
        :type position: Vec2d
        """
        self.game = game
        self.physics = physics
        self.color = subclass.COLOR
        self.body = Body(body_type=Body.STATIC)
        self.body.position = position
        self.physics.add(self.body)
        if isinstance(shape, pymunk.Shape):
            self.shape = self.add_shape(shape, subclass)
        elif type(shape) == list:
            self.shape = [self.add_shape(s, subclass) for s in shape]

        self.lastpoint = Vec(0, 0)
        self.eq = None
        self.length = None
        self.marcked = False

    def add_shape(self, shape: pymunk.Shape, subclass) -> pymunk.Shape:
        s = shape
        s.body = self.body
        s.friction = subclass.FRICTION
        s.color = self.color
        s.elasticity = ELASTICITY
        s.collision_type = 3
        self.physics.add(s)
        return s

    def update(self) -> None:
        pass

    @property
    @abstractmethod
    def drawing_shapes(self):
        pass

    @property
    @abstractmethod
    def texture_manager(self):
        pass

    def draw(self) -> None:
        offset = self.body.position * self.game.zoom - self.game.camera.position + self.game.displacement
        for group, tex in self.drawing_shapes:
            points = [(p + self.body.position) * self.game.zoom - self.game.camera.position + self.game.displacement
                      for p in group]
            try:
                pygame.gfxdraw.textured_polygon(self.game.screen, points,
                                                scale(self.texture_manager.textures[tex], zoom=self.game.zoom),
                                                round(offset.x), -round(offset.y))
            except pygame.error:
                pass

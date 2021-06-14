import pymunk
from pymunk import Vec2d, Body as Vec, Body
from settings.FLOORS import *
from abc import ABC, abstractmethod
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

    @abstractmethod
    def draw(self) -> None:
        pass

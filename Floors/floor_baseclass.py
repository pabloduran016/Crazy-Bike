import pymunk
from pymunk import Vec2d, Body as Vec, Body
from settings.FLOORS import *
from abc import ABC, abstractmethod
# from game import Physics


class Floor(ABC):
    def __init__(self, game, physics, position, subclass, shape):
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

    def add_shape(self, shape, subclass):
        s = shape
        s.body = self.body
        s.friction = subclass.FRICTION
        s.color = self.color
        s.elasticity = ELASTICITY
        s.collision_type = 3
        self.physics.add(s)
        return s

    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

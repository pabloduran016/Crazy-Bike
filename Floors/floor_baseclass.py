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
        if isinstance(shape, pymunk.Shape):
            self.shape = shape
            self.shape.body = self.body
            self.shape.friction = subclass.FRICTION
            self.shape.color = self.color
            self.shape.elasticity = ELASTICITY
            self.shape.collision_type = 3
            self.physics.add(self.body, self.shape)
        elif type(shape) == list:
            self.shape = []
            self.physics.add(self.body)
            for s in shape:
                s.body = self.body
                s.friction = subclass.FRICTION
                s.color = self.color
                s.collision_type = 3
                s.elasticity = ELASTICITY
                self.shape.append(s)
                self.physics.add(s)
        self.lastpoint = Vec(0, 0)
        self.eq = None
        self.length = None
        self.marcked = False

    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

import pymunk as pk
from pymunk import Vec2d as Vec
from typing import Union


class Physics:
    space: pk.Space
    gravity: Vec

    def update(self):
        self.space.step(0.5)
        self.space.step(0.5)

    def start_space(self, gravity):
        self.space = pk.Space()
        self.space.gravity = gravity
        self.gravity = gravity

    def add(self, *args: Union[pk.Shape, pk.Body, pk.Constraint]):
        for obj in args:
            self.space.add(obj)

    def reset(self):
        self.start_space(self.gravity)

    def remove(self, *args: Union[pk.Shape, pk.Body, pk.Constraint]):
        for obj in args:
            self.space.remove(obj)

import pymunk as pk
from pymunk import Vec2d as Vec
from typing import Union, Tuple


class Physics:
    space: pk.Space
    gravity: Vec

    def __init__(self, game):
        self.game = game

    def update(self) -> None:
        self.space.step(0.5)
        self.space.step(0.5)

    def start_space(self, gravity: Union[Tuple[float, float], Vec]) -> None:
        self.space = pk.Space()
        self.space.gravity = gravity
        self.gravity = gravity

    def add(self, *args: Union[pk.Shape, pk.Body, pk.Constraint]) -> None:
        for obj in args:
            self.space.add(obj)

    def reset(self) -> None:
        self.start_space(gravity=self.gravity)

    def remove(self, *args: Union[pk.Shape, pk.Body, pk.Constraint]) -> None:
        for obj in args:
            self.space.remove(obj)

    def coin_collected(self, arbiter: pk.arbiter.Arbiter, space: pk.Space, data: dict) -> bool:
        for shape in arbiter.shapes:
            shape: pk.Shape
            if hasattr(shape, 'activated'):
                shape.activated = False
                self.game.coins_collected += 1
        return True

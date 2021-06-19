from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
from settings.FLOORS import *
import settings.FLOORS as FLOORS
from typing import Union, Tuple


class Parabola(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], length: float, height: float, width: float,
                 n_segments: int = 10, up: bool = True, **kwargs):
        if up:
            self.a = height/length ** 2
            points1 = [Vec(x * length / n_segments, self.a * (x * length / n_segments) ** 2)
                       for x in range(n_segments + 1)]

        else:
            self.a = -height/length**2
            points1 = [Vec(x * length / n_segments + length, self.a * (x * length / n_segments) ** 2 + height)
                       for x in range(-n_segments, 0)]

        points2 = [v + Vec(0, width) for v in reversed(points1)]
        points3 = [v + Vec(0, 20) for v in reversed(points1)]
        points4 = [v + Vec(0, BORDER_WIDTH) for v in reversed(points1)]
        self.points = points1 + points2
        self.grass = points1 + points3
        self.border = points1 + points4
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        if up:
            self.eq = lambda x: self.a * (x ** 2)

        else:
            self.eq = lambda x: self.a * ((x - self.length) ** 2) + self.height

    @property
    def drawing_shapes(self):
        return (self.points, TEXTURES['ground']), (self.grass, TEXTURES['grass']), (self.border, TEXTURES['border'])

    @property
    def texture_manager(self):
        return self.game.texture_manager


class ParabolaUp(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], length: float, height: float, width: float,
                 n_segments: int = 10, **kwargs):
        self.a = height/length**2
        points1 = [Vec(x*length/n_segments, self.a*(x*length/n_segments)**2) for x in range(n_segments)]
        points2 = [v + Vec(0, width) for v in reversed(points1)]
        points3 = [v + Vec(0, 20) for v in reversed(points1)]
        self.points = points1 + points2
        self.grass = points1 + points3
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        self.eq = lambda x: self.a*(x**2)

    @property
    def drawing_shapes(self):
        return (self.points, TEXTURES['ground']), (self.grass, TEXTURES['grass'])

    @property
    def texture_manager(self):
        return self.game.texture_manager


class ParabolaDown(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], length: float, height: float, width: float,
                 n_segments: int = 10, **kwargs):
        self.a = -height/length**2
        points1 = [Vec(x*length/n_segments + length, self.a*(x*length/n_segments)**2 + height)
                   for x in range(-n_segments, 0)]
        points2 = [v + Vec(0, width) for v in reversed(points1)]
        points3 = [v + Vec(0, 20) for v in reversed(points1)]
        self.points = points1 + points2
        self.grass = points1 + points3
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        self.eq = lambda x: self.a*((x - self.length)**2) + self.height

    @property
    def drawing_shapes(self):
        return (self.points, TEXTURES['ground']), (self.grass, TEXTURES['grass'])

    @property
    def texture_manager(self):
        return self.game.texture_manager

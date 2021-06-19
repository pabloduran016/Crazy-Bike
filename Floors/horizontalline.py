from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
from settings.FLOORS import *
import settings.FLOORS as FLOORS
from typing import Tuple, Union


class HorizontalLine(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], length: float, width: float, **kwargs):
        """
        :type position: Vec2d
        :type length: float
        :type width: int
        """
        shape = Segment(body=None, a=(0, 0), b=(length, 0), radius=RADIUS)
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.length = length
        self.width = width
        self.fill = FILL
        self.lastpoint = Vec(length, 0) + position
        self.ground = [Vec(0, 20), Vec(length, 20), Vec(length, width), Vec(0, width)]
        self.grass = [Vec(0, 0), Vec(length, 0), Vec(length, 20), Vec(0, 20)]
        self.border = [Vec(0, 0), Vec(length, 0), Vec(length, BORDER_WIDTH), Vec(0, BORDER_WIDTH)]
        self.slope = 0
        self.eq = lambda x: 0

    @property
    def drawing_shapes(self):
        return (self.ground, TEXTURES['ground']), (self.grass, TEXTURES['grass']), (self.border, TEXTURES['border'])

    @property
    def texture_manager(self):
        return self.game.texture_manager

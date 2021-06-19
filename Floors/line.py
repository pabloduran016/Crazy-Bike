from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
from settings.FLOORS import *
import settings.FLOORS as FLOORS
from typing import Union, Tuple


class Line(Floor):
    def __init__(self, position: Union[Vec, Tuple[float, float]], final_pos: Union[Vec, Tuple[float, float]],
                 width: float, **kwargs):
        """
        :type position: Vec2d
        :type final_pos: Vec2d
        :type width: int
        """
        shape = Segment(body=None, a=(0, 0), b=final_pos-position, radius=RADIUS)
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.width = width
        self.length = (final_pos - position).x
        self.height = (final_pos - position).y
        self.fill = FILL
        self.lastpoint = Vec(final_pos[0], final_pos[1])
        self.ground = [Vec(0, 0), self.lastpoint - position, self.lastpoint - position + Vec(0, self.width),
                       Vec(0, self.width)]
        self.grass = [Vec(0, 0), self.lastpoint - position, self.lastpoint - position + Vec(0, 20),
                         Vec(0, 20)]
        self.border = [Vec(0, 0), self.lastpoint - position, self.lastpoint - position + Vec(0, BORDER_WIDTH),
                         Vec(0, BORDER_WIDTH)]
        self.slope = self.height/self.length
        self.eq = lambda p: self.slope*p

    @property
    def drawing_shapes(self):
        return (self.ground, TEXTURES['ground']), (self.grass, TEXTURES['grass']), (self.border, TEXTURES['border'])

    @property
    def texture_manager(self):
        return self.game.texture_manager

from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
import pygame
import pygame.gfxdraw
from settings.FLOORS import *
import settings.FLOORS as FLOORS
from functions import scale


class Parabola(Floor):
    def __init__(self, game, position, length, height, width, n_segments=10, up=True):
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
        self.points = points1 + points2
        self.grass = points1 + points3
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        if up:
            self.eq = lambda x: self.a * (x ** 2)

        else:
            self.eq = lambda x: self.a * ((x - self.length) ** 2) + self.height

    def draw(self):
        offset = self.body.position*self.game.zoom - self.game.camera
        for group, tex in ((self.points, 'ground'), (self.grass, 'grass')):
            points = [(p + self.body.position)*self.game.zoom - self.game.camera + self.game.displacement
                      for p in group]
            try:
                pygame.gfxdraw.textured_polygon(self.game.screen, points,
                                                scale(self.game.textures[tex], self.game.zoom),
                                                round(offset.x), -round(offset.y))
            except pygame.error:
                pass


class ParabolaUp(Floor):
    def __init__(self, game, position, length, height, width, n_segments=10):
        self.a = height/length**2
        points1 = [Vec(x*length/n_segments, self.a*(x*length/n_segments)**2) for x in range(n_segments)]
        points2 = [v + Vec(0, width) for v in reversed(points1)]
        points3 = [v + Vec(0, 20) for v in reversed(points1)]
        self.points = points1 + points2
        self.grass = points1 + points3
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        self.eq = lambda x: self.a*(x**2)

    def draw(self):
        points = [(p + self.body.position)*self.game.zoom - self.game.camera + self.game.displacement
                  for p in self.points]
        offset = self.body.position*self.game.zoom - self.game.camera
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.game.textures['ground'], round(offset.x),
                                            -round(offset.y))
        except pygame.error:
            pass
        points = [(vertice + self.body.position)*self.game.zoom - self.game.camera + self.game.displacement
                  for vertice in self.grass]
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.game.textures['grass'], round(offset.x),
                                            -round(offset.y))
        except pygame.error:
            pass


class ParabolaDown(Floor):
    def __init__(self, game, position, length, height, width, n_segments=10):
        self.a = -height/length**2
        points1 = [Vec(x*length/n_segments + length, self.a*(x*length/n_segments)**2 + height)
                   for x in range(-n_segments, 0)]
        points2 = [v + Vec(0, width) for v in reversed(points1)]
        points3 = [v + Vec(0, 20) for v in reversed(points1)]
        self.points = points1 + points2
        self.grass = points1 + points3
        shape = [Segment(None, a=points1[i-1], b=p, radius=RADIUS) for i, p in enumerate(points1) if i != 0]
        super().__init__(game=game, position=position, subclass=FLOORS, shape=shape)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        self.eq = lambda x: self.a*((x - self.length)**2) + self.height

    def draw(self):
        points = [(p + self.body.position)*self.game.zoom - self.game.camera + self.game.displacement
                  for p in self.points]
        offset = self.body.position*self.game.zoom - self.game.camera
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.game.textures['ground'], round(offset.x),
                                            -round(offset.y))
        except pygame.error:
            pass
        points = [(vertice + self.body.position)*self.game.zoom - self.game.camera + self.game.displacement
                  for vertice in self.grass]
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.game.textures['grass'], round(offset.x),
                                            -round(offset.y))
        except pygame.error:
            pass

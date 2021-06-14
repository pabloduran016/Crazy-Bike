from .floor_baseclass import Floor
from pymunk import Vec2d as Vec
from pymunk import Segment
import pygame
import pygame.gfxdraw
from settings.FLOORS import *
import settings.FLOORS as FLOORS
from Utilities import scale


class Parabola(Floor):
    def __init__(self, position, length, height, width, n_segments=10, up=True, **kwargs):
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
        super().__init__(position=position, subclass=FLOORS, shape=shape, **kwargs)
        self.length = length
        self.lastpoint = points1[-1] + self.body.position
        self.width = width
        self.height = height
        self.fill = FILL
        self.texture_manager = self.game.texture_manager
        if up:
            self.eq = lambda x: self.a * (x ** 2)

        else:
            self.eq = lambda x: self.a * ((x - self.length) ** 2) + self.height

    def draw(self):
        offset = self.body.position*self.game.zoom - self.game.camera.position + self.game.displacement
        for group, tex in ((self.points, 'ground'), (self.grass, 'grass')):
            points = [(p + self.body.position)*self.game.zoom - self.game.camera.position + self.game.displacement
                      for p in group]
            try:
                pygame.gfxdraw.textured_polygon(self.game.screen, points,
                                                scale(self.texture_manager.textures[tex], zoom=self.game.zoom),
                                                round(offset.x), -round(offset.y))
            except pygame.error:
                pass


class ParabolaUp(Floor):
    def __init__(self, position, length, height, width, n_segments=10, **kwargs):
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
        self.texture_manager = self.game.texture_manager
        self.eq = lambda x: self.a*(x**2)

    def draw(self):
        points = [(p + self.body.position)*self.game.zoom - self.game.camera.position + self.game.displacement
                  for p in self.points]
        offset = self.body.position*self.game.zoom - self.game.camera.position
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.texture_manager.textures['ground'],
                                            round(offset.x), -round(offset.y))
        except pygame.error:
            pass
        points = [(vertice + self.body.position)*self.game.zoom - self.game.camera.position + self.game.displacement
                  for vertice in self.grass]
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.texture_manager.textures['grass'],
                                            round(offset.x), -round(offset.y))
        except pygame.error:
            pass


class ParabolaDown(Floor):
    def __init__(self, position, length, height, width, n_segments=10, **kwargs):
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
        self.texture_manager = self.game.texture_manager
        self.eq = lambda x: self.a*((x - self.length)**2) + self.height

    def draw(self):
        points = [(p + self.body.position)*self.game.zoom - self.game.camera.position + self.game.displacement
                  for p in self.points]
        offset = self.body.position*self.game.zoom - self.game.camera.position
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.texture_manager.textures['ground'],
                                            round(offset.x), -round(offset.y))
        except pygame.error:
            pass
        points = [(vertice + self.body.position)*self.game.zoom - self.game.camera.position + self.game.displacement
                  for vertice in self.grass]
        try:
            pygame.gfxdraw.textured_polygon(self.game.screen, points, self.texture_manager.textures['grass'],
                                            round(offset.x), -round(offset.y))
        except pygame.error:
            pass

import pygame
from Utilities import pivotjoint, scale, blitrotate
from settings.BOARD import *
from pymunk import Vec2d as Vec
import pymunk
from typing import Union, Tuple
# from game import Physics


class Board(pygame.sprite.Sprite):
    available_costumes: set
    pivot: Vec
    dimensions: tuple
    body: pymunk.Body
    shape: pymunk.Shape
    joint1: pymunk.Constraint
    joint2: pymunk.Constraint
    handler: pymunk.CollisionHandler
    angle: float

    def __init__(self, game, physics, body_a, body_b, costume: str = 'bike'):
        """
        :type game: game.Game
        :param body_a First Body you want to attach
        :type body_a: wheel.Wheel
        :param body_b Second Body you want to attach
        :type body_b: wheel.Wheel
        """
        super().__init__()
        self.game = game
        self.physics = physics
        self.color = COLOR
        self.thetaacc = THETAACC
        self.available_costumes = COSTUMES.keys()
        self.load_costume(costume)
        self.body_a = body_a
        self.body_b = body_b
        # Pymunk Body for the board
        self.load_physics()
        self.flipped = False
        self.costume = costume
        self.checkground = 1

    def load_costume(self, costume: str) -> None:
        self.costume = costume
        self.game.data['costumes']['board'] = costume
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.pivot = Vec(*COSTUMES[costume]['pivot'])
        self.dimensions = COSTUMES[costume]['dimensions']

    def load_physics(self) -> None:
        self.angle = (self.body_b.body.position - self.body_a.body.position).get_angle_degrees_between(Vec(1, 0))
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.body_a.body.position
        self.shape = pymunk.Poly(self.body, VERICES)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 2
        self.shape.filter = pymunk.ShapeFilter(group=2)
        self.physics.add(self.body, self.shape)
        self.joint1 = pivotjoint(self.body, self.body_a.body)
        self.joint1.collide_bodies = False
        self.joint2 = pivotjoint(self.body, self.body_b.body, a=self.body_b.body.position - self.body.position)
        self.joint2.collide_bodies = False
        self.physics.add(self.joint1, self.joint2)
        self.handler = self.physics.space.add_collision_handler(2, 3)
        self.handler.begin = self.check_ground_begin

    def reset(self) -> None:
        self.load_physics()
        self.checkground = 1
        self.flipped = False

    def next_costume(self) -> str:
        costumes = list(self.available_costumes)
        for i, costume in enumerate(costumes):
            if costume == self.costume:
                if len(costumes) == i + 1:
                    return costumes[0]
                else:
                    return costumes[i + 1]

    def change_costume_to(self, costume: str) -> None:
        if costume in self.available_costumes:
            if costume != self.costume:
                self.load_costume(costume)
        else:
            raise ValueError(f'Costume {costume} not known')

    def update(self) -> None:
        if not self.game.crushed:
            self.body.angular_velocity *= AIR_DRAG_MULTIPLIER
            self.angle = round((self.body_b.body.position -
                                self.body_a.body.position).get_angle_degrees_between(Vec(1, 0)))
            if -100 < self.angle < -80 and not self.flipped:
                self.game.flips += 1
                self.flipped = True
            elif self.angle > 0 and self.flipped:
                self.flipped = False
        else:
            dic = self.physics.space._constraints.copy()
            for con in dic:
                self.game.physics.remove(con)
            # im, pos = blitrotate(self.image, self.body.position - self.game.camera.position, self.pivot, self.angle)
            # self.game.screen.blit(im, pos)
            self.game.physics.space.gravity = (0, 0)
            self.body.velocity = (0, 0)
            self.body.angular_velocity = 0
            self.shape.sensor = True

    def draw(self) -> None:
        im, pos = blitrotate(scale(self.image, self.dimensions, self.game.zoom),
                             self.body.position*self.game.zoom - self.game.camera.position + self.game.displacement,
                             self.pivot*self.game.zoom, self.angle)
        # print(im.get_size())
        self.game.screen.blit(im, pos)

    def check_ground_begin(self, arbiter, space, data) -> bool:
        if not self.game.crushed:
            self.game.crushed = True
            if not self.game.camera.shake:
                self.game.camera.shake = 10
        return True


class SimpleBoard:
    def __init__(self, position: Union[Vec, Tuple[float, float]], costume:str):
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.available_costumes = COSTUMES.keys()
        self.pivot = Vec(*COSTUMES[costume]['pivot'])
        self.dimensions = COSTUMES[costume]['dimensions']
        self.costume = costume
        self.position = Vec(*position)
        self.rect = self.image.get_rect()
        self.rect.topleft = position - self.pivot
        # self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        # self.dimensions = dimensions
        # self.rect = pygame.Rect(0, 0, *dimensions)
        # self.pivot = Vec(*COSTUMES[costume]['pivot'])
        # self.rect.center =  - self.pivot + position
        # self.available_costumes = COSTUMES.keys()

    def draw(self, screen: Union[pygame.Surface, pygame.SurfaceType]) -> None:
        # print(im.get_size())
        im = pygame.transform.scale(self.image, self.dimensions)
        rect = im.get_rect()
        pivot = self.pivot[0]*self.dimensions[0]/COSTUMES[self.costume]['dimensions'][0],\
                self.pivot[1]*self.dimensions[1]/COSTUMES[self.costume]['dimensions'][1]
        rect.topleft = self.position - pivot
        screen.blit(im, rect)

    def change_costume_to(self, costume: str) -> None:
        if costume in self.available_costumes:
            if costume != self.costume:
                self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
                self.available_costumes = COSTUMES.keys()
                self.pivot = Vec(*COSTUMES[costume]['pivot'])
                self.dimensions = COSTUMES[costume]['dimensions']
                self.costume = costume
                self.rect = self.image.get_rect()
                self.rect.topleft = self.position - self.pivot
        else:
            raise ValueError(f'Costume {costume} not known')

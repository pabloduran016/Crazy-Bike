import pygame
import pymunk
from pymunk import Vec2d as Vec
from settings.WHEEL import *
from Utilities import scale ,blitrotate, rad_to_degrees
import random
from abc import ABC, abstractmethod
# from game import Physics
# from functions import load_svg


class Wheel(pygame.sprite.Sprite, ABC):
    def __init__(self, game, physics, costume='bike'):
        """
        :type game: game.Game
        """
        super().__init__()
        self.game = game
        self.physics = physics
        self.color = COLOR
        self.radius = RADIUS
        self.width = WIDTH
        self.thetaacc = THETAACC
        # self.image = load_svg(IMAGE, size=DIMENSIONS).convert_alpha()
        self.costume = costume
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.dimensions = COSTUMES[costume]['dimensions']
        self.available_costumes = COSTUMES.keys()
        self.initial_position = Vec(0, 0)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.initial_position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.physics.add(self.body, self.shape)
        self.shape.filter = pymunk.ShapeFilter(group=1)

    def next_costume(self) -> str:
        costumes = iter(self.available_costumes)
        costume = next(costumes)
        while self.costume == costume:
            costume = next(costumes)
        return costume

    @abstractmethod
    def get_id(self):
        pass

    def change_costume_to(self, costume: str) -> None:
        # print('hello')
        if costume in self.available_costumes:
            if costume != self.costume:
                self.game.data['costumes'][self.get_id()] = costume
                self.costume = costume
                self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
                self.dimensions = COSTUMES[costume]['dimensions']
            else:
                print(f'Costume {costume} is already being used')
        else:
            raise ValueError(f'Costume {costume} not known')

    def update(self):
        if self.game.crushed:
            self.body.angular_velocity = random.randint(-300, 300)/100
            self.shape.sensor = True

    def reset(self):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.initial_position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.physics.add(self.body, self.shape)
        self.shape.filter = pymunk.ShapeFilter(group=1)

    def draw(self):
        # if not self.game.crushed:
        im = scale(self.image, self.dimensions, self.game.zoom)
        rect = im.get_rect()
        # print(rect.size)
        rect.center = self.body.position*self.game.zoom - self.game.camera + self.game.displacement
        self.game.screen.blit(*blitrotate(im, Vec(*rect.center), Vec(rect.width/2, rect.height/2),
                                          rad_to_degrees(-self.body.angle)))
        # pygame.draw.circle(self.game.screen, self.color, self.body.position-self.game.camera, self.radius, self.width)


class SimpleWheel:
    def __init__(self, position, costume):
        self.costume = costume
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.dimensions = COSTUMES[costume]['dimensions']
        self.rect = pygame.Rect(0, 0, *self.dimensions)
        self.rect.center = position
        self.available_costumes = COSTUMES.keys()

    def change_costume_to(self, costume: str) -> None:
        if costume in self.available_costumes:
            if costume != self.costume:
                self.costume = costume
                self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        else:
            raise ValueError(f'Costume {costume} not known')

    def draw(self, screen):
        # print(rect.size)
        im = pygame.transform.scale(self.image, self.dimensions)
        rect = im.get_rect()
        rect.center = self.rect.center
        screen.blit(im, rect)


class FrontWheel(Wheel):
    def __init__(self, *args, **kwargs):
        super(FrontWheel, self).__init__(*args, **kwargs)
        self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION) + Vec(DISTANCE, 0)

    def get_id(self):
        return 'frontwheel'


class BackWheel(Wheel):
    def __init__(self, *args, **kwargs):
        super(BackWheel, self).__init__(*args, **kwargs)
        self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION)
        self.handler = self.physics.space.add_collision_handler(1, 3)
        self.handler.begin = self.check_ground_begin
        self.handler.separate = self.check_ground_separate
        self.handler.pre_solve = self.check_ground_presolve

    def get_id(self):
        return 'backwheel'

    def reset(self):
        super(BackWheel, self).reset()
        self.handler = self.physics.space.add_collision_handler(1, 3)
        self.handler.begin = self.check_ground_begin
        self.handler.separate = self.check_ground_separate
        self.handler.pre_solve = self.check_ground_presolve

    def update(self):
        self.body.angular_velocity *= AIR_DRAG_MULTIPLIER
        super().update()

    def check_ground_presolve(self, arbiter, space, data):
        self.game.board.checkground = 0
        if self.game.airtime:
            # print('begin', self.game.board.checkground)
            self.game.airtime = 0
        return True

    def check_ground_begin(self, arbiter, space, data):
        if self.game.airtime:
            # print('begin', self.game.board.checkground)
            self.game.airtime = 0
        if not self.game.camera_shake and self.body.velocity.y > 15:
            # print('shake')
            self.game.camera_shake = 8
        return True

    def check_ground_separate(self, arbiter, space, data):
        self.game.board.checkground = 1
        if not self.game.airtime:
            # print('separate', self.game.board.checkground)
            self.game.airtime = 1
        return True

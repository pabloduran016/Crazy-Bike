import pygame.image
from Utilities import pivotjoint, scale, blitrotate
from settings.BOARD import *
import pymunk.vec2d
# from game import Physics
vec = pymunk.Vec2d


class Board(pygame.sprite.Sprite):
    def __init__(self, game, physics, body_a, body_b, costume='bike'):
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
        # Spring
        self.body_a = body_a
        self.body_b = body_b
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.available_costumes = COSTUMES.keys()
        self.pivot = vec(*COSTUMES[costume]['pivot'])
        self.dimensions = COSTUMES[costume]['dimensions']
        self.angle = (self.body_b.body.position - self.body_a.body.position).get_angle_degrees_between(vec(1, 0))
        # Pymunk Body for the board
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
        self.checkground = 1
        self.handler = self.physics.space.add_collision_handler(2, 3)
        self.handler.begin = self.check_ground_begin
        self.flipped = False
        self.costume = costume

    def reset(self):
        self.angle = (self.body_b.body.position - self.body_a.body.position).get_angle_degrees_between(vec(1, 0))
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
        self.checkground = 1
        self.handler = self.physics.space.add_collision_handler(2, 3)
        self.handler.begin = self.check_ground_begin
        self.flipped = False

    def next_costume(self) -> str:
        costumes = iter(self.available_costumes)
        costume = next(costumes)
        while self.costume == costume:
            costume = next(costumes)
        return costume

    def change_costume_to(self, costume: str) -> None:
        if costume in self.available_costumes:
            if costume != self.costume:
                self.costume = costume
                self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
                self.pivot = vec(*COSTUMES[costume]['pivot'])
                self.dimensions = COSTUMES[costume]['dimensions']
        else:
            raise ValueError(f'Costume {costume} not known')

    def update(self):
        if not self.game.crushed:
            self.body.angular_velocity *= AIR_DRAG_MULTIPLIER
            self.angle = round((self.body_b.body.position -
                                self.body_a.body.position).get_angle_degrees_between(vec(1, 0)))
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
            self.game.physics.gravity = (0, 0)
            self.body.velocity = (0, 0)
            self.body.angular_velocity = 0
            self.shape.sensor = True

    def draw(self):
        im, pos = blitrotate(scale(self.image, self.dimensions, self.game.zoom),
                             self.body.position*self.game.zoom - self.game.camera.position + self.game.displacement,
                             self.pivot*self.game.zoom, self.angle)
        # print(im.get_size())
        self.game.screen.blit(im, pos)

    def check_ground_begin(self, arbiter, space, data):
        if not self.game.crushed:
            self.game.crushed = True
            if not self.game.camera.shake:
                self.game.camera.shake = 10
        return True


class SimpleBoard:
    def __init__(self, position, costume):
        self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        self.available_costumes = COSTUMES.keys()
        self.pivot = vec(*COSTUMES[costume]['pivot'])
        self.dimensions = COSTUMES[costume]['dimensions']
        self.costume = costume
        self.position = vec(*position)
        self.rect = self.image.get_rect()
        self.rect.topleft = position - self.pivot
        # self.image = pygame.image.load(COSTUMES[costume]['image']).convert_alpha()
        # self.dimensions = dimensions
        # self.rect = pygame.Rect(0, 0, *dimensions)
        # self.pivot = vec(*COSTUMES[costume]['pivot'])
        # self.rect.center =  - self.pivot + position
        # self.available_costumes = COSTUMES.keys()

    def draw(self, screen):
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
                self.pivot = vec(*COSTUMES[costume]['pivot'])
                self.dimensions = COSTUMES[costume]['dimensions']
                self.costume = costume
                self.rect = self.image.get_rect()
                self.rect.topleft = self.position - self.pivot
        else:
            raise ValueError(f'Costume {costume} not known')

import pygame.image
from joints import pivotjoint
from settings.BOARD import *
import pymunk.vec2d
from functions import scale, blitrotate
vec = pymunk.Vec2d


class Board(pygame.sprite.Sprite):
    def __init__(self, game, body_a, body_b):
        """
        :type game: main.Game
        :param body_a First Body you want to attach
        :type body_a: wheel.Wheel
        :param body_b Second Body you want to attach
        :type body_b: wheel.Wheel
        """
        super().__init__()
        self.game = game
        self.color = COLOR
        self.thetaacc = THETAACC
        # Spring
        self.body_a = body_a
        self.body_b = body_b
        self.image = pygame.image.load(IMAGE).convert_alpha()
        self.pivot = vec(*PIVOT)
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
        self.game.space.add(self.body, self.shape)
        self.joint1 = pivotjoint(self.body, self.body_a.body)
        self.joint1.collide_bodies = False
        self.joint2 = pivotjoint(self.body, self.body_b.body, a=self.body_b.body.position - self.body.position)
        self.joint2.collide_bodies = False
        self.game.space.add(self.joint1, self.joint2)
        self.checkground = 1
        self.handler = self.game.space.add_collision_handler(2, 3)
        self.handler.begin = self.check_ground_begin
        self.flipped = False

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
            dic = self.game.space._constraints.copy()
            for con in dic:
                self.game.space.remove(con)
            im, pos = blitrotate(self.image, self.body.position - self.game.camera, self.pivot, self.angle)
            self.game.screen.blit(im, pos)
            self.game.space.gravity = (0, 0)
            self.body.velocity = (0, 5)
            self.shape.sensor = True

    def draw(self):
        im, pos = blitrotate(scale(self.image, DIMENSIONS, self.game.zoom),
                             self.body.position*self.game.zoom - self.game.camera + self.game.displacement,
                             self.pivot*self.game.zoom, self.angle)
        # print(im.get_size())
        self.game.screen.blit(im, pos)

    def reset(self):
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        self.angle = 0
        self.body.position = self.body_a.body.position

    def check_ground_begin(self, arbiter, space, data):
        self.game.crushed = True
        return True

import pygame
import pymunk
from pymunk import Vec2d as Vec
from settings.WHEEL import *
from functions import blitrotate, scale, rad_to_degrees
# from functions import load_svg


class Wheel(pygame.sprite.Sprite):
    def __init__(self, game, identity):
        """
        :type game: main.Game
        :type identity: str
        :param identity Frontwheel or Backwheel
        """
        super().__init__()
        self.game = game
        self.id = identity
        assert self.id == 'backwheel' or self.id == 'frontwheel', \
            f'INVALID ID, expected frontwheel or backwheel, got {identity}'
        self.color = COLOR
        self.radius = RADIUS
        self.width = WIDTH
        self.thetaacc = THETAACC
        # self.image = load_svg(IMAGE, size=DIMENSIONS).convert_alpha()
        self.image = pygame.image.load(IMAGE).convert_alpha()
        if self.id == 'backwheel':
            self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION)
        elif self.id == 'frontwheel':
            self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION) + Vec(DISTANCE, 0)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.initial_position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.game.space.add(self.body, self.shape)
        self.shape.filter = pymunk.ShapeFilter(group=1)
        if self.id == 'backwheel':
            self.handler = self.game.space.add_collision_handler(1, 3)
            self.handler.begin = self.check_ground_begin
            self.handler.separate = self.check_ground_separate

    def update(self):
        if self.id == 'backwheel':
            self.body.angular_velocity *= AIR_DRAG_MULTIPLIER
        if self.game.crushed:
            if self.id == 'bakcwheel':
                self.body.velocity = (2, -5)
            elif self.id == 'frontwheel':
                self.body.velocity = (-2, -5)
            self.shape.sensor = True

    def draw(self):
        # if not self.game.crushed:
        im = scale(self.image, DIMENSIONS, self.game.zoom)
        rect = im.get_rect()
        # print(rect.size)
        rect.center = self.body.position*self.game.zoom - self.game.camera + self.game.displacement
        self.game.screen.blit(*blitrotate(im, Vec(*rect.center), Vec(rect.width/2, rect.height/2),
                                          rad_to_degrees(-self.body.angle)))
        # pygame.draw.circle(self.game.screen, self.color, self.body.position-self.game.camera, self.radius, self.width)

    def reset(self):
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        if self.id == 'backwheel':
            self.body.position += (0, -100)
        if self.id == 'frontwheel':
            self.body.position = self.game.backwheel.body.position + (90, 0)

    def check_ground_begin(self, arbiter, space, data):
        self.game.board.checkground = 0
        return True

    def check_ground_separate(self, arbiter, space, data):
        self.game.board.checkground = 1
        return True

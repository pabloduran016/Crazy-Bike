import pymunk
import pygame
from pymunk import Vec2d as Vec
from math import sin, pi
from settings.COIN import *
from pygame import Surface, SurfaceType
from typing import List, Union, Optional, Any
# from game import Physics


class Coin:
    def __init__(self, game, physics=None, position=(0, 0), phase=0):
        """
        :type game: game.Game
        :type position: Vec2d
        """
        self.position = position
        self.game = game
        assert 0 <= phase <= IDLE_ANIM_SIZE - 1, f'phase should be between 0 and COIN.ANIMATION_SIZE - 1; was {phase}'
        self.phase = phase
        self.rect = pygame.Rect((0, 0, DIMENSIONS[0], DIMENSIONS[1]))
        self.rect.center = self.position
        self.physics = physics
        if physics is not None:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body.position = position
            self.shape = pymunk.Circle(self.body, 35/2)
            self.shape.activated = True
            self.ended = False
            self.collected_counter = 0
            self.shape.collision_type = 4
            self.shape.sensor = True
            self.physics.add(self.body, self.shape)
            self.handler = self.physics.space.add_collision_handler(2, 4)
            self.handler.begin = self.physics.coin_collected
        self.displacement = Vec(0, 0)

    def __str__(self):
        return f'position: {self.position}, phase: {self.phase}, activated: {self.shape.activated}'

    def update(self):
        self.displacement = Vec(0, AMPLITUD * sin(pi / 2 + (self.phase*2*pi/(IDLE_ANIM_SIZE - 1)) +
                                                  DISPLACEMENT_OMEGA * pygame.time.get_ticks() / 1000))
        # self.body.position += self.displacement
        # print(f'{self.displacement.y:.2f}')

    def draw(self):
        pass


class SimpleCoin(pygame.sprite.Sprite):
    displacement = Vec(0, 0)

    def __init__(self, game: Any, position, period=2, phase=0, moving: bool=False,
                 images: Optional[List[Union[Surface, SurfaceType]]]=None):
        """
        :type game: Optional[main.py.Game, None]
        :type position: tuple
        :type period: float
        """
        super().__init__()
        self.game = game
        if images is None:
            self.images = [pygame.transform.scale(
                pygame.image.load(IDLE_ANIM + f'{(x + IDLE_OFFSET):04}.png').convert_alpha(), DIMENSIONS)
                                for x in range(IDLE_ANIM_SIZE)]
        else:
            self.images = [image for image in (pygame.transform.scale(img, DIMENSIONS) for img in images)]
        self.counter = - phase
        assert 0 <= phase <= IDLE_ANIM_SIZE - 1, f'phase should be between 0 and {IDLE_ANIM_SIZE - 1}; was {phase}'
        self.phase = phase
        self.period = period
        self.rect = pygame.Rect((0, 0, DIMENSIONS[0], DIMENSIONS[1]))
        self.rect.right = position[0] - 10
        self.rect.centery = position[1]
        self.moving = moving

    def update(self):
        self.counter += 1 / self.period
        if round(self.counter) + self.phase > IDLE_ANIM_SIZE - 1:
            self.counter = - self.phase
        if self.moving:
            self.displacement = Vec(0, AMPLITUD * sin(pi / 2 + (self.phase * 2 * pi / (IDLE_ANIM_SIZE - 1)) +
                                                  DISPLACEMENT_OMEGA * pygame.time.get_ticks() / 1000))

    def draw(self, screen=None):
        counter = round(self.counter) + self.phase
        assert 0 <= counter <= IDLE_ANIM_SIZE - 1, \
            f'Counter must be between 0 and {IDLE_ANIM_SIZE - 1}, was {counter}'
        rect = self.images[counter].get_rect()
        rect.center = self.rect.center + self.displacement
        if self.game is not None:
            self.game.screen.blit(self.images[counter], rect)
        else:
            screen.blit(self.images[counter], rect)

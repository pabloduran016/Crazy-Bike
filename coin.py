import pymunk
import pygame
from settings.COIN import *


class Coin:
    def __init__(self, game, position, phase=0):
        """
        :type game: main.Game
        :type position: Vec2d
        """
        self.position = position
        self.game = game
        assert 0 <= phase <= IDLE_ANIM_SIZE - 1, f'phase should be between 0 and COIN.ANIMATION_SIZE - 1; was {phase}'
        self.phase = phase
        self.rect = pygame.image.load(IDLE_ANIM + '0.png').get_rect()
        self.rect.center = self.position
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 35/2)
        self.shape.activated = True
        self.ended = False
        self.collected_counter = 0
        self.shape.collision_type = 4
        self.shape.sensor = True
        self.game.space.add(self.body, self.shape)
        self.handler = self.game.space.add_collision_handler(2, 4)
        self.handler.begin = self.game.coin_collected

    def __str__(self):
        return f'position: {self.position}, phase: {self.phase}, activated: {self.shape.activated}'

    def update(self):
        pass

    def draw(self):
        pass

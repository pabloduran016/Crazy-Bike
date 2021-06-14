import pygame
from pymunk import Vec2d as Vec
from settings.FOREGROUND import *


class Foreground(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        :type game: game.Game
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load(IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.multiplier = MULTIPLIER
        self.initial_pos = INITIAL_POS

    def update(self):
        pass

    def draw(self) -> None:
        cam = self.game.camera.position * self.multiplier
        x = int(cam.x / self.rect.width)
        y = 0
        for disp in ((0, 0), (1, 0), (-1, 0)):
            position = Vec((x + disp[0]) * self.rect.width, (y + disp[1]) * self.rect.height) - cam
            self.game.screen.blit(self.image, position)

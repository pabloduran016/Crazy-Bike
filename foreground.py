import pygame
import pymunk
from settings.FOREGROUND import *
vec = pymunk.Vec2d


class Foreground(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        :type game: main.Game
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load(IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.multiplier = MULTIPLIER

    def update(self):
        pass

    def draw(self):
        cam = vec((self.game.camera * self.multiplier).x, self.game.camera.y - 50)
        x = int(cam.x / self.rect.width)
        y = 0
        for disp in ((0, 0), (1, 0), (-1, 0)):
            position = ((x + disp[0]) * self.rect.width, (y + disp[1]) * self.rect.height)
            self.game.screen.blit(self.image, - cam + position)

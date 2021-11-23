import pygame
from settings.BACKGROUND import *
from pymunk import Vec2d as Vec


class Background(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        :type game: game.Game
        """
        super().__init__()
        self.game = game
        self.sky_image = pygame.image.load(SKY_IMAGE).convert_alpha()
        self.mountain_image = pygame.transform.scale(pygame.image.load(MOUNTAIN_IMAGE).convert_alpha(), MOUNTAIN_DIMENSIONS)
        self.sky_rect = self.sky_image.get_rect()
        self.mountain_rect = self.mountain_image.get_rect()
        self.sky_multiplier = SKY_MULTIPLIER
        self.mountain_multiplier = MOUNTAIN_MULTIPLIER
        self.mountain_intial_position = MOUNTAIN_INITIAL_POSITION

    def update(self):
        pass

    def draw(self) -> None:
        # SKY
        cam = self.game.camera.position * self.sky_multiplier
        x = int(cam.x / self.sky_rect.width)
        y = int(cam.y / self.sky_rect.height)
        for disp in ((0, 0), (0, 1), (1, 0), (1, 1), (0, -1), (1, -1), (-1, 0), (-1, -1), (-1, 1)):
            position = ((x + disp[0]) * self.sky_rect.width, (y + disp[1]) * self.sky_rect.height) - cam
            self.game.screen.blit(self.sky_image, position)
        # MOUNTAINS
        cam = self.game.camera.position * self.mountain_multiplier
        x = int(cam.x / self.mountain_rect.width)
        y = 0
        for disp in ((0, 0), (1, 0), (-1, 0)):
            position = Vec((x + disp[0]) * self.mountain_rect.width, (y + disp[1]) * self.mountain_rect.height) + \
                       self.mountain_intial_position - cam
            self.game.screen.blit(self.mountain_image, position)

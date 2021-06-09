import pygame as pg
from typing import Tuple


class Button:
    function = lambda x: None

    def __init__(self, image, size, center):
        self.image = pg.transform.scale(pg.image.load(image), size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center

    def mouseclick(self, mouse):
        if self.is_clicked(mouse):
            return self.function()

    def bind(self, function):
        self.function = function

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse: Tuple[float]) -> bool:
        if self.rect.left <= mouse[0] <= self.rect.right and self.rect.top <= mouse[1] <= self.rect.bottom:
            return True
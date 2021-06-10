import pygame as pg
from typing import Tuple


class Button:
    function = lambda x: None

    def __init__(self, size, center, image=None, color=None):
        self.image = pg.transform.scale(pg.image.load(image), size).convert_alpha() if image is not None else None
        self.rect = pg.Rect(0, 0, *size)
        self.rect.center = center
        self.color = color

    def mouseclick(self, mouse):
        if self.is_clicked(mouse):
            return self.function()

    def bind(self, function):
        self.function = function

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def is_clicked(self, mouse: Tuple[float]) -> bool:
        if self.rect.left <= mouse[0] <= self.rect.right and self.rect.top <= mouse[1] <= self.rect.bottom:
            return True
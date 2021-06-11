import pygame as pg
from typing import Tuple, Callable, Dict, Any


class Button:
    function = lambda x: None

    def __init__(self, size, center, image=None, color=None):
        self.image = pg.transform.scale(pg.image.load(image), size).convert_alpha() if image is not None else None
        self.rect = pg.Rect(0, 0, *size)
        self.rect.center = center
        self.color = color
        self.instructions: Dict[str, Callable[[*Any, Any], None]] = {}

    def set_instrucion(self, instruction: str, function: Callable[[Any, Any], Any]):
        if instruction not in self.instructions.keys():
            self.instructions[instruction] = function
    
    def mouseclick(self, mouse):
        if self.is_clicked(mouse):
            return self.function()

    def bind(self, function):
        self.function = function

    def draw(self, screen):
        if 'draw' in self.instructions.keys():
            return self.instructions['draw'](self, screen)
        else:
            if self.image is not None:
                screen.blit(self.image, self.rect)
            else:
                pg.draw.rect(screen, self.color, self.rect)

    def is_clicked(self, mouse: Tuple[float]) -> bool:
        if self.rect.left <= mouse[0] <= self.rect.right and self.rect.top <= mouse[1] <= self.rect.bottom:
            return True
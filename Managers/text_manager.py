from typing import Tuple, Any, List, Union, Callable, Dict
from Utilities import formated
import pygame as pg
import pygame.freetype as pg_ft



class Text:
    font: pg_ft.Font
    rect: pg.Rect
    text: str
    color: List[int]
    size: int
    visible: bool
    formating: Any

    def __init__(self, font: pg_ft.Font, text: str, color: List[int], size: int, visible: bool, formating: Any):
        self.font = font
        self.rect = self.font.get_rect(text=formated(text, formating), size=size)
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.formating = formating


class TextManager:
    text: List[Text] = []
    function: Callable = None

    def __init__(self, font: pg_ft.Font):
        self.font: pg_ft.Font = font

    def add_text(self, text: str, color: List[int], size: int, visible: bool, formating: Any, **kwargs) -> None:
        t = Text(self.font, text, color, size, visible, formating)
        for key, value in kwargs.items():
            if hasattr(t.rect, key):
                t.rect.__setattr__(key, value)
        self.text.append(t)

    def bulk_adding(self, *args: Tuple[str, Tuple[int], int, bool, Any,
                                       Dict[str, Union[Tuple[float, float], float]]]) -> None:
        for arg in args:
            self.add_text(*[a for a in arg if type(a) != dict], **arg[-1] if type(arg[-1]) == dict else {'': None})

    def draw(self, screen: Union[pg.Surface, pg.SurfaceType]) -> None:
        for text in iter(self.text):
            if text.visible:
                screen.blit(self.font.render(
                        text=formated(text.text, text.formating),
                        fgcolor=text.color,
                        size=text.size)[0], text.rect)

    def set_text_update(self, function: Callable) -> None:
        self.function = function

    def update(self) -> None:
        if self.function is not None:
            return self.function()

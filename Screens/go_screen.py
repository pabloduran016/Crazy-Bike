from settings.GOSCREEN import *
from Managers import TextManager
from typing import Union, Tuple, Optional
from Widgets import Button
from Utilities import scale
import pygame as pg
from settings import FPS
from .screen_baseclass import Screen

class GoScreen(Screen):
    def __init__(self, game):
        super(GoScreen, self).__init__()
        self.count = -.5
        self.game = game
        self.f_color = BLACK
        self.text_manager = TextManager(self.game.font)
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.text[1].formating = self.game.data['coins']
        self.text_manager.text[2].formating = self.game.flips
        self.text_manager.text[5].formating = self.game.points
        self.text_manager.text[6].formating = self.game.data['highscore']
        self.text_manager.update_rects()
        self.text_manager.set_text_update(self.text_update)

        self.store_button = Button(image=STORE_BUTTON_IMAGE,
                                   size=STORE_BUTTON_SIZE,
                                   center=STORE_BUTTON_center,
                                   color=WHITE)
        self.store_button.bind(self.store_click)
        self.store_button.set_instrucion('draw', self.store_button_draw)

    def store_click(self) -> bool:
        self.game.waiting = False
        self.game.screens_manager.current_screen = 'store'
        return True

    @staticmethod
    def store_button_draw(button: Button, screen: Union[pg.Surface, pg.SurfaceType]) -> None:
        pg.draw.rect(screen, button.color, button.rect)
        pg.draw.rect(screen, BLACK, button.rect, width=4)
        if button.image is not None:
            im = scale(button.image, zoom=0.8)
            rect = im.get_rect()
            rect.center = button.rect.center
            screen.blit(im, rect)

    def setup(self) -> None:
        self.game.waiting = True
        self.game.all_sprites.remove(self)
        self.reset()

    def __enter__(self):
        self.reset()
        self.game.waiting = True
        self.game.all_sprites.add(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.all_sprites.remove(self)

    def mouseclick(self, mouse: Tuple[int, int]) -> Optional[bool]:
        return self.store_button.mouseclick(mouse)

    def run(self) -> None:
        self.game.clock.tick(FPS)
        self.game.update()
        self.game.events()
        self.game.screen.fill(WHITE)
        self.game.all_sprites.draw()
        self.update()
        self.draw()
        pg.display.flip()

    def reset(self) -> None:
        self.count = -.5
        self.text_manager.reset()
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.text[1].formating = self.game.data['coins']
        self.text_manager.text[2].formating = self.game.flips
        self.text_manager.text[5].formating = self.game.points
        self.text_manager.text[6].formating = self.game.data['highscore']
        self.text_manager.update_rects()

    def update(self) -> None:
        self.count += 1/20
        if round(self.count) > ANIMATION_SIZE - 1:
            self.count = -.5
        self.text_manager.update()

    def text_update(self) -> None:
        self.text_manager.text[0].color = BLACK if round(self.count) == 0 else WHITE
        self.text_manager.text[3].color = BLACK if round(self.count) == 0 else WHITE
        self.text_manager.text[4].color = WHITE if round(self.count) == 0 else BLACK

    def draw(self) -> None:
        self.text_manager.draw(self.game.screen)
        self.store_button.draw(self.game.screen)

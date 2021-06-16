from settings.STARTSCREEN import *
import pygame as pg
from Managers import TextManager
from Sprites import SimpleCoin
from Widgets import Button
from typing import Union, Tuple, Optional
from Utilities.functions import scale


class StartScreen(pg.sprite.Sprite):
    def __init__(self, game):
        super(StartScreen, self).__init__()
        self.game = game
        self.image = pg.image.load(IMAGE).convert_alpha()
        self.count = -.5
        self.simple_coin = SimpleCoin(self.game, (0, 0), images=self.game.coin_manager.idle_images)
        self.text_manager = TextManager(self.game.font)
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.set_text_update(self.text_update)
        self.text_manager.text[2].formating = self.game.data['coins']
        self.text_manager.text[3].formating = self.game.data['highscore']
        self.text_manager.update_rects()
        self.simple_coin.rect.right = self.text_manager.text[2].rect.left - 30
        self.simple_coin.rect.centery = self.text_manager.text[2].rect.centery
        self.store_button = Button(image=STORE_BUTTON_IMAGE,
                                   size=STORE_BUTTON_SIZE,
                                   center=STORE_BUTTON_center,
                                   color=WHITE)
        self.store_button.bind(self.store_click)
        self.store_button.set_instrucion('draw', self.store_button_draw)

    @staticmethod
    def store_button_draw(button: Button, screen: Union[pg.Surface, pg.SurfaceType]):
        pg.draw.rect(screen, button.color, button.rect)
        pg.draw.rect(screen, BLACK, button.rect, width=4)
        if button.image is not None:
            im = scale(button.image, zoom=0.8)
            rect = im.get_rect()
            rect.center = button.rect.center
            screen.blit(im, rect)

    def reset(self) -> None:
        self.text_manager.reset()
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.text[2].formating = self.game.data['coins']
        self.text_manager.text[3].formating = self.game.data['highscore']
        self.text_manager.update_rects()
        self.simple_coin.rect.right = self.text_manager.text[2].rect.left - 30
        self.simple_coin.rect.centery = self.text_manager.text[2].rect.centery

    def mouseclick(self, mouse: Tuple[int, int]) -> Optional[bool]:
        return self.store_button.mouseclick(mouse)

    def store_click(self) -> bool:
        self.game.current_screen = 'store'
        self.game.store_screen.text_manager.text[6].visible = False
        self.game.waiting = False
        return True

    def update(self) -> None:
        self.count += 1/20
        if round(self.count) > ANIMATION_SIZE - 1:
            self.count = -.5
        self.simple_coin.update()
        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'
        self.text_manager.update()

    def text_update(self) -> None:
        self.text_manager.text[0].color = BLACK if round(self.count) == 0 else WHITE
        self.text_manager.text[1].color = BLACK if round(self.count) == 0 else WHITE

    def draw(self) -> None:
        self.game.screen.blit(self.image, (0, 0))
        self.text_manager.draw(self.game.screen)
        self.store_button.draw(self.game.screen)
        self.simple_coin.draw()

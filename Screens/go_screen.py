from settings.GOSCREEN import *
from Managers import TextManager
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

    def __enter__(self):
        self.game.waiting = True
        self.reset()

    def setup(self) -> None:
        self.game.waiting = True
        self.reset()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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

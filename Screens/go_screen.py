from settings.GOSCREEN import *
from Managers import TextManager


class GoScreen:
    def __init__(self, game):
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

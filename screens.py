from settings import STARTSCREEN, GOSCREEN, STORESCREEN, TEXTURES
from settings.FONTS import *
from pygame.image import load
from settings.colors import *
from functions import formated
from button import Button
import pygame as pg
from coin import SimpleCoin
from wheel import Wheel
from board import Board
from typing import Union
from store_item import StoreItem
from wheel import SimpleWheel


class StoreScreen(pg.sprite.Sprite):
    def __init__(self, game):
        super(StoreScreen, self).__init__()
        self.image = load(STORESCREEN.IMAGE)
        self.game = game
        self.count = 0
        self.texts = []
        self.wood_texture = pg.image.load(TEXTURES.WOOD).convert()
        self.simple_coin = SimpleCoin(self.game, (0, 0))
        self.simple_frontwheel = SimpleWheel(
            position=(STORESCREEN.BACKWHEEL_POSITION[0] + STORESCREEN.WHEELS_DISTANCE,
                      STORESCREEN.BACKWHEEL_POSITION[1]),
            costume=self.game.frontwheel.costume,
            dimensions=STORESCREEN.WHEELS_DIMENSIONS)
        self.simple_backwheel = SimpleWheel(
            position=STORESCREEN.BACKWHEEL_POSITION,
            costume=self.game.backwheel.costume,
            dimensions=STORESCREEN.WHEELS_DIMENSIONS)
        self.store_items = [StoreItem(
            font=self.game.font,
            size=item[1],
            text=item[0],
            price=item[4],
            dimensions=STORESCREEN.ITEM_DIMENSIONS,
            image=item[3],
            topleft=(item[2][0]*(STORESCREEN.ITEM_DIMENSIONS[0] + STORESCREEN.ITEM_SPACING) + STORESCREEN.ITEM_SPACING,
                     item[2][1]*STORESCREEN.ITEM_DIMENSIONS[0] + 220),
            texture=self.wood_texture,
            obj=item[5])
            for item in STORESCREEN.ITEMS]
        self.setup_fonts()

    def setup_fonts(self):
        self.texts = [
            [self.game.font.get_rect(text=f"CRAZY BIKE", size=STORESCREEN.CB_SIZE), f"CRAZY BIKE", BLACK,
             STORESCREEN.CB_SIZE, True, None],
            [self.game.font.get_rect(text=f"STORE", size=STORESCREEN.STORE_SIZE), f"STORE", BLACK,
             STORESCREEN.STORE_SIZE, True, None],
            [self.game.font.get_rect(text="PRESS SPACE TO START", size=STORESCREEN.SPACE_SIZE),
             "PRESS SPACE TO START", BLACK, STORESCREEN.SPACE_SIZE, True, None],
            [self.game.font.get_rect(text="PRESS M TO RETURN TO MENU", size=STORESCREEN.M_SIZE),
             "PRESS M TO RETURN TO MENU", BLACK, STORESCREEN.M_SIZE, True, None],
            [self.game.font.get_rect(text=f"{self.game.data['coins']}", size=STORESCREEN.SPACE_SIZE),
             f"{self.game.data['coins']}", BLACK, STORESCREEN.COINS_SIZE, True, None],
            [self.game.font.get_rect(text=f"HIGH SCORE: {self.game.data['highscore']}", size=HS_SIZE),
             "HIGH SCORE: {}", BLACK, HS_SIZE, True, self.game.data['highscore']]
        ]
        self.texts[0][0].center = STORESCREEN.CB_center
        self.texts[1][0].center = STORESCREEN.STORE_center
        self.texts[2][0].center = STORESCREEN.SPACE_center
        self.texts[3][0].center = STORESCREEN.M_center
        self.texts[4][0].topright = STORESCREEN.COINS_topright
        self.texts[5][0].centerx, self.texts[5][0].top = HS_topcenter

        self.simple_coin.rect.right = self.texts[4][0].left - 30
        self.simple_coin.rect.centery = self.texts[4][0].centery

    def mouseclick(self, mouse):
        for item in self.store_items:
            if item.button.is_clicked(mouse):
                if item.price < self.game.data['coins']:
                    if item.obj == 'wheel':
                        self.purchase(self.game.backwheel, item.item)
                        self.purchase(self.game.frontwheel, item.item)
                    elif item.obj == 'board':
                        self.purchase(self.game.board, item.item)

    def reset(self):
        self.setup_fonts()

    @staticmethod
    def purchase(obj: Union[Wheel, Board], costume: str) -> None:
        print(obj, costume)
        if costume in obj.available_costumes:
            obj.change_costume_to(costume)
        else:
            ValueError(f'Costume {costume} not known for {obj}')

    def update(self):
        self.count += 1/20
        if round(self.count) > STARTSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5
        self.simple_coin.update()
        for item in self.store_items:
            item.update()
        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'

    def draw(self):
        self.game.screen.blit(self.image, (0, 0))
        self.texts[0][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[1][2] = WHITE if round(self.count) == 0 else BLACK
        self.texts[2][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[3][2] = WHITE if round(self.count) == 0 else BLACK
        for rect, text, color, size, activated, value in self.texts:
            if activated:
                self.game.screen.blit(self.game.font.render(
                    text=formated(text, value),
                    fgcolor=color,
                    size=size)[0], rect)
        self.simple_coin.draw()
        self.simple_frontwheel.draw(self.game.screen)
        self.simple_backwheel.draw(self.game.screen)
        for item in self.store_items:
            item.draw(self.game.screen)


class StartScreen(pg.sprite.Sprite):
    def __init__(self, game):
        super(StartScreen, self).__init__()
        self.game = game
        self.image = load(STARTSCREEN.IMAGE).convert_alpha()
        self.count = -.5
        self.texts = []
        self.simple_coin = SimpleCoin(self.game, (0, 0))
        self.setup_fonts()
        self.store_button = Button(image=STARTSCREEN.STORE_BUTTON_IMAGE,
                                   size=STARTSCREEN.STORE_BUTTON_SIZE,
                                   center=STARTSCREEN.STORE_BUTTON_center)
        self.store_button.bind(self.store_click)

    def setup_fonts(self):
        self.texts = [
            [self.game.font.get_rect(text=f"CRAZY BIKE", size=STARTSCREEN.CB_SIZE), f"CRAZY BIKE", BLACK,
             STARTSCREEN.CB_SIZE, True, None],
            [self.game.font.get_rect(text="PRESS SPACE TO CONTINUE", size=STARTSCREEN.SPACE_SIZE),
             "PRESS SPACE TO CONTINUE", BLACK, STARTSCREEN.SPACE_SIZE, True, None],
            [self.game.font.get_rect(text=f"{self.game.data['coins']}", size=STARTSCREEN.SPACE_SIZE),
             f"{self.game.data['coins']}", BLACK, STARTSCREEN.COINS_SIZE, True, None],
            [self.game.font.get_rect(text=f"HIGH SCORE: {self.game.data['highscore']}", size=HS_SIZE),
             "HIGH SCORE: {}", BLACK, HS_SIZE, True, self.game.data['highscore']]
        ]
        self.texts[0][0].center = STARTSCREEN.CB_center
        self.texts[1][0].center = STARTSCREEN.SPACE_center
        self.texts[2][0].topright = STARTSCREEN.COINS_topright
        self.texts[3][0].centerx, self.texts[3][0].top = HS_topcenter

        self.simple_coin.rect.right = self.texts[2][0].left - 30
        self.simple_coin.rect.centery = self.texts[2][0].centery

    def reset(self):
        self.setup_fonts()

    def mouseclick(self, mouse):
        return self.store_button.mouseclick(mouse)

    def store_click(self):
        self.game.current_screen = 'store'
        self.game.waiting = False
        return True

    def update(self):
        self.count += 1/20
        if round(self.count) > STARTSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5
        self.simple_coin.update()
        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'

    def draw(self):
        self.game.screen.blit(self.image, (0, 0))
        self.texts[0][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[1][2] = BLACK if round(self.count) == 0 else WHITE
        for rect, text, color, size, activated, value in self.texts:
            if activated:
                self.game.screen.blit(self.game.font.render(
                    text=formated(text, value),
                    fgcolor=color,
                    size=size)[0], rect)
        self.store_button.draw(self.game.screen)
        self.simple_coin.draw()


class GoScreen:
    def __init__(self, game):
        self.count = -.5
        self.game = game
        self.f_color = BLACK
        self.texts = [
            [self.game.font.get_rect(text=f"GAME OVER", size=GOSCREEN.GO_SIZE), f"GAME OVER", GREY, GOSCREEN.GO_SIZE,
             True, None],
            [self.game.font.get_rect(text=f"{self.game.data['coins']}", size=CC_SIZE),
             f"{self.game.data['coins']}", BLACK, CC_SIZE, True, None],
            [self.game.font.get_rect(text=f"FLIPS {self.game.flips}", size=FLIPS_SIZE), f"FLIPS {self.game.flips}",
             BLACK, FLIPS_SIZE, False, None],
            [self.game.font.get_rect(text=f"PRESS SPACE TO RESTART", size=GOSCREEN.SPACE_SIZE),
             f"PRESS SPACE TO RESTART",
              BLACK, GOSCREEN.SPACE_SIZE, True, None],
            [self.game.font.get_rect(text=f"PRESS M TO GO TO MENU", size=GOSCREEN.MENU_SIZE), f"PRESS M TO GO TO MENU",
              BLACK, GOSCREEN.MENU_SIZE, True, None],
            [self.game.font.get_rect(text=f"{self.game.points:.0f}", size=POINTS_SIZE), f"{self.game.points:.0f}",
             BLACK, POINTS_SIZE, True, None],
        ]
        self.texts[0][0].center = GOSCREEN.GO_center
        self.texts[1][0].topright = CC_topright
        self.texts[2][0].topright = FLIPS_topright
        self.texts[3][0].center = GOSCREEN.SPACE_center
        self.texts[4][0].center = GOSCREEN.MENU_center
        self.texts[5][0].center = POINTS_center

    def update(self):
        self.count += 1/20
        if round(self.count) > GOSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5

    def draw(self, screen):
        self.texts[0][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[3][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[4][2] = WHITE if round(self.count) == 0 else BLACK
        for rect, text, color, size, activated, value in self.texts:
            if activated:
                screen.blit(self.game.font.render(
                    text=formated(text, value),
                    fgcolor=color,
                    size=size)[0], rect)

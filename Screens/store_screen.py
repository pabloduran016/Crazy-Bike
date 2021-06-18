from settings.STORESCREEN import *
import pygame as pg
from settings import FPS
from Player import SimpleWheel, SimpleBoard, Wheel, Board
from typing import List, Union
from .store_item import StoreItem
from settings import TEXTURES
from Sprites import SimpleCoin
from Managers import TextManager
from .screen_baseclass import Screen


class StoreScreen(Screen):
    simple_frontwheel: SimpleWheel
    simple_backwheel: SimpleWheel
    simple_board: SimpleBoard
    store_items: List[StoreItem]
    count = 0
    image = pg.image.load(IMAGE)

    def __init__(self, game):
        super(StoreScreen, self).__init__()
        self.game = game
        self.wood_texture = pg.image.load(TEXTURES.WOOD).convert()
        self.simple_coin = SimpleCoin(self.game, (0, 0), images=self.game.coin_manager.idle_images)
        self.setup_simple_bike()
        self.text_manager = TextManager(self.game.font)
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.set_text_update(self.text_update)
        self.text_manager.text[4].formating = self.game.data['coins']
        self.text_manager.text[5].formating = self.game.data['highscore']
        self.text_manager.update_rects()
        self.simple_coin.rect.right = self.text_manager.text[4].rect.left - 30
        self.simple_coin.rect.centery = self.text_manager.text[4].rect.centery
        self.store_items = self.load_items()

    def __enter__(self):
        self.reset()
        self.game.waiting = True
        self.game.coin_manager.reset(ss=True)
        self.game.all_sprites.add(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.all_sprites.remove(self)

    def setup(self) -> None:
        self.reset()
        self.game.waiting = True
        self.game.coin_manager.reset(ss=True)
        self.game.all_sprites.add(self)

    def run(self) -> None:
        self.game.events()
        self.game.screen.fill(WHITE)
        self.update()
        self.draw()
        pg.display.flip()
        self.game.clock.tick(FPS)

    def setup_simple_bike(self) -> None:
        self.simple_frontwheel = SimpleWheel(
            position=(BACKWHEEL_POSITION[0] + WHEELS_DISTANCE,
                      BACKWHEEL_POSITION[1]),
            costume=self.game.frontwheel.costume)
        self.simple_backwheel = SimpleWheel(
            position=BACKWHEEL_POSITION,
            costume=self.game.backwheel.costume)
        self.simple_board = SimpleBoard(
            position=BACKWHEEL_POSITION,
            costume=self.game.board.costume)

    def load_items(self) -> List[StoreItem]:
        return [StoreItem(
            font=self.game.font,
            size=item[1],
            text=item[0],
            price=item[4],
            dimensions=ITEM_DIMENSIONS,
            image_height=ITEM_IMAGE_DIMENSIONS,
            image=item[3],
            topleft=(item[2][0] * (ITEM_DIMENSIONS[0] +
                                   ITEM_SPACING[0]) + ITEM_SPACING[0],
                     item[2][1] * (ITEM_DIMENSIONS[1] +
                                   ITEM_SPACING[1]) + ITEM_INITIAL_POSITION[1]),
            texture=self.wood_texture,
            obj=item[5],
            images=self.game.coin_manager.idle_images)
            for item in ITEMS]

    def mouseclick(self, mouse) -> None:
        for item in self.store_items:
            if item.button.is_clicked(mouse):
                # print(item.price, self.game.data['coins'])
                # TODO: fix bugs, sometimes you can buy with not enough coins and you end up eith negative coins
                if item.price <= self.game.data['coins']:
                    item.color = GREY
                    self.text_manager.text[6].visible = False
                    if item.obj == 'wheel':
                        self.purchase(self.game.backwheel, item.item, item.price)
                        self.simple_backwheel.change_costume_to(item.item)
                        self.purchase(self.game.frontwheel, item.item, item.price)
                        self.simple_frontwheel.change_costume_to(item.item)
                    elif item.obj == 'board':
                        self.purchase(self.game.board, item.item, item.price)
                        self.simple_board.change_costume_to(item.item)
                else:
                    # print('you have not enough coins')
                    self.text_manager.text[6].visible = True
                    item.color = RED
            else:
                item.color = WHITE

    def reset(self) -> None:
        self.text_manager.reset()
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.text[4].formating = self.game.data['coins']
        self.text_manager.text[5].formating = self.game.data['highscore']
        self.text_manager.update_rects()

        self.simple_coin.rect.right = self.text_manager.text[4].rect.left - 30
        self.simple_coin.rect.centery = self.text_manager.text[4].rect.centery

    def purchase(self, obj: Union[Wheel, Board], costume: str, price: int) -> None:
        self.game.data['coins'] -= price
        if costume in obj.available_costumes:
            obj.change_costume_to(costume)
        else:
            ValueError(f'Costume {costume} not known for {obj}')

    def update(self) -> None:
        self.count += 1/20
        if round(self.count) > ANIMATION_SIZE - 1:
            self.count = -.5
        self.simple_coin.update()
        for item in self.store_items:
            item.update()
        self.text_manager.update()
        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'

    def text_update(self) -> None:
        self.text_manager.text[0].color = BLACK if round(self.count) == 0 else WHITE
        self.text_manager.text[1].color = WHITE if round(self.count) == 0 else BLACK
        self.text_manager.text[2].color = BLACK if round(self.count) == 0 else WHITE
        self.text_manager.text[3].color = WHITE if round(self.count) == 0 else BLACK
        self.text_manager.text[4].formating = self.game.data['coins']

    def draw(self) -> None:
        self.game.screen.blit(self.image, (0, 0))
        self.text_manager.draw(self.game.screen)
        self.simple_coin.draw()
        self.simple_frontwheel.draw(self.game.screen)
        self.simple_backwheel.draw(self.game.screen)
        self.simple_board.draw(self.game.screen)
        for item in self.store_items:
            item.draw(self.game.screen)

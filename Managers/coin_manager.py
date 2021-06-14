import pygame as pg
from pymunk import Vec2d as Vec
from settings.COIN import *
from settings.colors import *
from Sprites.coin import Coin
from random import randrange
from Utilities import scale
from typing import List, Union


class CoinManager(pg.sprite.Sprite):
    def __init__(self, game, physics, period=1.5, ss=False):
        """
        :type game: game.Game
        """
        super().__init__()
        self.idle = IDLE_ANIM
        self.collected = COLLECTED_ANIM
        self.idle_images = self.load_images(IDLE_ANIM, IDLE_OFFSET, IDLE_ANIM_SIZE)
        # self.collected_images = [pg.image.load(self.collected + f'{x}.png').convert_alpha()
        #                          for x in range(COLLECTED_ANIM_SIZE)]
        self.rect = pg.Rect(0, 0, DIMENSIONS[0], DIMENSIONS[1])
        self.game = game
        self.physics = physics
        self.coins = []
        self.space = SPACING
        self.count = 0
        self.period = period
        self.ss = ss

    @staticmethod
    def load_images(path: str, offset: int, size: int) -> List[Union[pg.Surface, pg.SurfaceType]]:
        try:
            return [pg.image.load(path + f'{(x + offset):04}.png').convert_alpha() for x in range(size)]
        except FileNotFoundError:
            print([IDLE_ANIM + f'{(x + IDLE_OFFSET):04}.png' for x in range(IDLE_ANIM_SIZE)])
            raise

    def reset(self, ss=False):
        self.coins = []
        self.count = 0
        self.ss = ss

    def start(self):
        pass

    def update(self):
        for coin in self.coins:
            coin.update()
        self.count += 1/self.period
        if round(self.count) > IDLE_ANIM_SIZE - 1:
            self.count = 0
        while len(self.coins) > 100:
            self.coins.pop(0)
        self.check_collected()

    def check_collected(self):
        for i, coin in enumerate(self.coins):
            if coin.physics is not None:
                if not coin.shape.activated:
                    coin.collected_counter += 15
                    if round(coin.collected_counter) > COLLECTED_ANIM_SIZE:
                        coin.collected_counter = 0
                        coin.ended = True
                if coin.ended:
                    self.physics.remove(coin.shape, coin.body)
                    self.coins.pop(i)
                pass

    def generate(self, floor):
        coin_x = floor.body.position.x
        coin_y = floor.body.position.y
        length = floor.length
        num = randrange(0, 3)
        if num == 1:
            for x in range(int((length - DISTANCE)/100)):
                if hasattr(floor, 'slope'):
                    s = floor.slope
                else:
                    if hasattr(floor, 'points'):
                        space = floor.length / (len(floor.points)/2)
                        p1 = floor.points[int((DISTANCE + x * 100) // space)]
                        p2 = floor.points[int((DISTANCE + x * 100) // space) + 1]
                        d = p2 - p1
                        s = 0 if d.x == 0 else d.y/d.x
                    else:
                        s = 0
                self.coins.append(Coin(self.game, self.physics,
                                       position=Vec(DISTANCE + x * 100 + coin_x,
                                                    coin_y + floor.eq(DISTANCE + x * 100)) + Vec(s, -1) * DISTANCE,
                                       phase=randrange(0, IDLE_ANIM_SIZE)))
        floor.marked = True
        pass

    def draw(self):
        if self.ss:
            for coin in self.coins:
                if round(self.count + coin.phase) > (IDLE_ANIM_SIZE - 1):
                    counter = round((self.count + coin.phase) - (IDLE_ANIM_SIZE - 1) *
                                    ((self.count + coin.phase) // (IDLE_ANIM_SIZE - 1)))
                else:
                    counter = round(self.count + coin.phase)
                assert 0 <= counter <= IDLE_ANIM_SIZE - 1, \
                    f'Counter must be between 0 and {IDLE_ANIM_SIZE - 1}, was {counter}'
                pos = coin.rect.topleft + coin.displacement
                self.game.screen.blit(scale(self.idle_images[counter], original_dimensions=DIMENSIONS,
                                            zoom=1), pos)
        else:
            for i, coin in enumerate(self.coins):
                if coin.shape.activated:
                    if round(self.count + coin.phase) > (IDLE_ANIM_SIZE - 1):
                        counter = round((self.count + coin.phase) - (IDLE_ANIM_SIZE - 1) *
                                        ((self.count + coin.phase) // (IDLE_ANIM_SIZE - 1)))
                    else:
                        counter = round(self.count + coin.phase)
                    assert 0 <= counter <= IDLE_ANIM_SIZE - 1, \
                        f'Counter must be between 0 and {IDLE_ANIM_SIZE - 1}, was {counter}'
                    pos = (coin.body.position - Vec(*self.rect.center) + coin.displacement)*self.game.zoom \
                          - self.game.camera.position + self.game.displacement
                    self.game.screen.blit(scale(self.idle_images[counter], original_dimensions=DIMENSIONS,
                                                    zoom=self.game.zoom), pos)
                else:
                    if round(coin.collected_counter) > (COLLECTED_ANIM_SIZE - 1):
                        counter = round(coin.collected_counter - (COLLECTED_ANIM_SIZE - 1) *
                                        (coin.collected_counter // (COLLECTED_ANIM_SIZE - 1)))
                    else:
                        counter = round(coin.collected_counter)
                    assert 0 <= counter <= COLLECTED_ANIM_SIZE - 1, \
                        f'Counter must be between 0 and {COLLECTED_ANIM_SIZE - 1}, was {counter}'
                    self.draw_collected(coin)

    def draw_collected(self, coin):
        width1 = (((coin.collected_counter + DIMENSIONS[0] / 4) / 100) * DIMENSIONS[0] / 2)
        width2 = DIMENSIONS[0] / 4 + DIMENSIONS[0] / 2 - (coin.collected_counter / 200) * (
                    DIMENSIONS[0] / 4 + DIMENSIONS[0] / 2)
        width = max(width1, width2)
        image = pg.Surface((width * 2, width * 2), pg.SRCALPHA)
        image.set_colorkey((255, 255, 255))
        rect = image.get_rect()
        pg.draw.circle(image, YELLOW[:3] + (int(255 - 255 * coin.collected_counter / 200),),
                       rect.center, width1)
        pg.draw.circle(image, WHITE[:3] + (int(255 - 255 * coin.collected_counter / 200),),
                       rect.center, width2)
        rect.center = coin.body.position + coin.displacement
        pos = (coin.body.position + coin.displacement) * self.game.zoom \
              - self.game.camera.position + self.game.displacement
        rect.center = pos
        self.game.screen.blit(image, rect)

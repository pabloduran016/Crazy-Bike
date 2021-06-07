import pygame as pg
from pymunk import Vec2d as Vec
from settings.COIN import *
from settings.colors import *
from coin import Coin
from random import randrange
from functions import scale


class CoinManager(pg.sprite.Sprite):
    def __init__(self, game, period=1.5, ss=False):
        """
        :type game: main.Game
        """
        super().__init__()
        self.idle = IDLE_ANIM
        self.collected = COLLECTED_ANIM
        try:
            self.idle_images = [pg.image.load(IDLE_ANIM + f'{(x + IDLE_OFFSET):04}.png').convert_alpha()
                                for x in range(IDLE_ANIM_SIZE)]
        except FileNotFoundError:
            print([IDLE_ANIM + f'{(x + IDLE_OFFSET):04}.png' for x in range(IDLE_ANIM_SIZE)])
            raise
        # self.collected_images = [pg.image.load(self.collected + f'{x}.png').convert_alpha()
        #                          for x in range(COLLECTED_ANIM_SIZE)]
        self.rect = pg.Rect(0, 0, DIMENSIONS[0], DIMENSIONS[1])
        # for img in self.collected_images:
        #     for x in range(img.get_width()):
        #         for y in range(img.get_height()):
        #             if img.get_at((x, y)) == (255, 255, 255):
        #                 a = img.get_at((x, y))[3]
        #                 img.set_at((x, y), (0, 0, 0, a))
        self.game = game
        self.coins = []
        self.space = SPACING
        self.count = 0
        self.period = period
        self.ss = ss

    def reset(self, ss=False):
        self.coins = []
        self.count = 0
        self.ss = ss

    def start(self):
        # self.coins += [Coin(self.game, position=Vec(150, 750), phase=0)]
        # self.coins += [Coin(self.game, position=Vec(250, 750), phase=1)]
        # # self.coins += [Coin(self.game, position=Vec(300, 750))]
        pass

    def update(self):
        for coin in self.coins:
            coin.update()
        self.count += 1/self.period
        if round(self.count) > IDLE_ANIM_SIZE - 1:
            self.count = 0
        while len(self.coins) > 100:
            self.coins.pop(0)
        lis = enumerate(self.coins)
        for i, coin in lis:
            if not coin.shape.activated:
                coin.collected_counter += 10
                if round(coin.collected_counter) > COLLECTED_ANIM_SIZE:
                    coin.collected_counter = 0
                    coin.ended = True
            if coin.ended:
                self.game.space.remove(coin.shape, coin.body)
                self.coins.pop(i)
            pass

    def generate(self, floor):
        coin_x = floor.body.position.x
        coin_y = floor.body.position.y
        length = floor.length
        num = randrange(0, 3)
        # num = 1
        # print(num)
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
                self.coins.append(Coin(self.game,
                                       position=Vec(DISTANCE + x * 100 + coin_x,
                                                    coin_y + floor.eq(DISTANCE + x * 100)) + Vec(s, -1) * DISTANCE,
                                       phase=randrange(0, IDLE_ANIM_SIZE)))
        floor.marked = True
        pass

    def draw(self):
        for i, coin in enumerate(self.coins):
            if coin.shape.activated:
                if round(self.count + coin.phase) > (IDLE_ANIM_SIZE - 1):
                    counter = round((self.count + coin.phase) - (IDLE_ANIM_SIZE - 1) *
                                    ((self.count + coin.phase) // (IDLE_ANIM_SIZE - 1)))
                else:
                    counter = round(self.count + coin.phase)
                assert 0 <= counter <= IDLE_ANIM_SIZE - 1, \
                    f'Counter must be between 0 and {IDLE_ANIM_SIZE - 1}, was {counter}'
                if not self.ss:
                    pos = (coin.body.position - Vec(*self.rect.center) + coin.displacement)*self.game.zoom \
                          - self.game.camera + self.game.displacement
                    self.game.screen.blit(scale(self.idle_images[counter], original_dimensions=DIMENSIONS,
                                                zoom=self.game.zoom), pos)
                else:
                    pos = coin.body.position - Vec(self.rect.centerx, self.rect.centery) + coin.displacement
                    self.game.screen.blit(scale(self.idle_images[counter], original_dimensions=DIMENSIONS,
                                                zoom=1), pos)
            else:
                if round(coin.collected_counter) > (COLLECTED_ANIM_SIZE - 1):
                    counter = round(coin.collected_counter - (COLLECTED_ANIM_SIZE - 1) *
                                    (coin.collected_counter // (COLLECTED_ANIM_SIZE - 1)))
                else:
                    counter = round(coin.collected_counter)
                assert 0 <= counter <= COLLECTED_ANIM_SIZE - 1, \
                    f'Counter must be between 0 and {COLLECTED_ANIM_SIZE - 1}, was {counter}'
                # if not self.ss:
                #     pos = (coin.body.position - Vec(*self.rect.center) + coin.displacement) * self.game.zoom \
                #           - self.game.camera + self.game.displacement
                #     # print(counter)
                #     self.game.screen.blit(scale(self.collected_images[counter], original_dimensions=DIMENSIONS,
                #                                 zoom=self.game.zoom), pos)
                # else:
                #     pos = coin.body.position - Vec(self.rect.centerx, self.rect.centery) + coin.displacement
                #     self.game.screen.blit(scale(self.collected_images[counter], original_dimensions=DIMENSIONS,
                #                                 zoom=1), pos)
                if not self.ss:
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
                          - self.game.camera + self.game.displacement
                    rect.center = pos
                    # pg.draw.rect(self.game.screen, BLACK, rect)
                    print(rect)
                    self.game.screen.blit(image, rect)

import pygame as pg
from pymunk import Vec2d as Vec
from settings.COIN import *
from coin import Coin
from random import randrange


class CoinManager(pg.sprite.Sprite):
    def __init__(self, game, period=3, ss=False):
        """
        :type game: main.Game
        """
        super().__init__()
        self.idle = IDLE_ANIM
        self.collected = COLLECTED_ANIM
        self.idle_images = [pg.image.load(self.idle + f'{x}.png').convert_alpha()
                                 for x in range(IDLE_ANIM_SIZE)]
        self.collected_images = [pg.image.load(self.collected + f'{x}.png').convert_alpha()
                                 for x in range(COLLECTED_ANIM_SIZE)]
        self.rect = self.idle_images[0].get_rect()
        # for img in self.collected_images:
        #     for x in range(img.get_width()):
        #         for y in range(img.get_height()):
        #             if img.get_at((x, y)) == (255, 255, 255):
        #                 a = img.get_at((x, y))[3]
        #                 img.set_at((x, y), (0, 0, 0, a))
        self.game = game
        self.coins = []
        self.space = SPACING
        self.pos = 1
        self.count = 0
        self.period = period
        self.ss = ss

    def start(self):
        # self.coins += [Coin(self.game, position=Vec(150, 750), phase=0)]
        # self.coins += [Coin(self.game, position=Vec(250, 750), phase=1)]
        # # self.coins += [Coin(self.game, position=Vec(300, 750))]
        pass

    def update(self):
        self.count += 1/self.period
        if round(self.count) > IDLE_ANIM_SIZE - 1:
            self.count = 0
        while len(self.coins) > 100:
            self.coins.pop(0)
        lis = enumerate(self.coins)
        for i, coin in lis:
            if not coin.shape.activated:
                coin.collected_counter += 1.2
                if round(coin.collected_counter) > COLLECTED_ANIM_SIZE - 1:
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
                    pos = coin.body.position*self.game.zoom - Vec(self.rect.centerx, self.rect.centery)*self.game.zoom\
                        - self.game.camera + self.game.displacement
                    self.game.screen.blit(pg.transform.scale(self.idle_images[counter],
                                                             (round(DIMENSIONS[0]*self.game.zoom),
                                                              round(DIMENSIONS[1]*self.game.zoom))), pos)
                else:
                    pos = coin.body.position - Vec(self.rect.centerx, self.rect.centery) - self.game.camera
                    self.game.screen.blit(self.idle_images[counter], pos)
            else:
                if round(coin.collected_counter) > (COLLECTED_ANIM_SIZE - 1):
                    counter = round(coin.collected_counter - (COLLECTED_ANIM_SIZE - 1) *
                                    (coin.collected_counter // (COLLECTED_ANIM_SIZE - 1)))
                else:
                    counter = round(coin.collected_counter)
                assert 0 <= counter <= IDLE_ANIM_SIZE - 1, \
                    f'Counter must be between 0 and {IDLE_ANIM_SIZE - 1}, was {counter}'
                if not self.ss:
                    pos = coin.body.position*self.game.zoom - Vec(self.rect.centerx, self.rect.centery)*self.game.zoom\
                      - self.game.camera + self.game.displacement
                    self.game.screen.blit(pg.transform.scale(self.collected_images[counter],
                                                            (round(DIMENSIONS[0] * self.game.zoom),
                                                             round(DIMENSIONS[1] * self.game.zoom))), pos)
                else:
                    pos = coin.body.position - Vec(self.rect.centerx, self.rect.centery) - self.game.camera
                    self.game.screen.blit(self.collected_images[counter], pos)

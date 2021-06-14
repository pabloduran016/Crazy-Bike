from settings import *
from pymunk import Vec2d as Vec
from Managers import *
import pygame as pg
from Sprites import *
from Utilities import *
import pygame.freetype as pg_ft
from settings.TEXT import *


class GameProperties:
    playing = running = waiting = True
    _crushed = False

    _coins_collected = _flips = _points = _pluspoints = _pluspoints_counter = _distance = _airtime = _lasty =\
        go_counter = delta_zoom = camera_shake = 0

    _zoom = ZOOM
    points_size = POINTS_SIZE
    displacement = DISPLACEMENT

    camera: Camera
    camera_focus: Vec
    scroll: Vec = Vec(0, 0)

    all_sprites: SpriteGroup
    backwheel: BackWheel
    frontwheel: FrontWheel
    board: Board
    background: Background

    current_screen: str
    screen: pg.Surface
    loading_screen: pg.Surface
    start_screen: StartScreen
    go_screen: GoScreen
    store_screen: StoreScreen

    floors_manager: FloorsManager
    coin_manager: CoinManager
    text_manager: TextManager
    data_manager: JsonManager
    texture_manager: TextureManager
    data: dict

    simple_coin: SimpleCoin
    clock: pg.time.Clock
    font: pg_ft.Font

    @property
    def lasty(self):
        return self._lasty

    @lasty.setter
    def lasty(self, value):
        self._lasty = value

    @property
    def coins_collected(self):
        return self._coins_collected

    @coins_collected.setter
    def coins_collected(self, value):
        self._coins_collected = value
        # self.texts[1] = self.font.get_rect(text=f"Coins Collected {self.coins_collected}", size=CC_SIZE)
        self.text_manager.text[1].rect = self.font.get_rect(text=f"{self.coins_collected + self.data['coins']}",
                                                            size=CC_SIZE)
        self.text_manager.text[1].rect.topright = CC_topright
        self.text_manager.text[1].formating = self.coins_collected + self.data['coins']
        self.simple_coin.rect.right = self.text_manager.text[1].rect.left - 30
        self.simple_coin.rect.centery = self.text_manager.text[1].rect.centery

    @property
    def flips(self):
        return self._flips

    @flips.setter
    def flips(self, value):
        self.pluspoints += value - self._flips
        self._flips = value
        self.text_manager.text[2].rect = self.font.get_rect(text=f"FLIPS {self.flips}", size=FLIPS_SIZE)
        self.text_manager.text[2].formating = self.flips
        self.text_manager.text[2].rect.topright = FLIPS_topright

    @property
    def crushed(self):
        return self._crushed

    @crushed.setter
    def crushed(self, value):
        if not self._crushed:
            self.points_size = POINTS_SIZE
            self._pluspoints_counter = 0
            self.data['coins'] += self._coins_collected
            self.data['highscore'] = self.points if self.points > self.data['highscore'] else self.data['highscore']
            self.text_manager.text[8].formating = self.data['highscore']
        self._crushed = value

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.displacement = self.camera.focus * (1 - self._zoom)
        self.text_manager.text[3].rect = self.font.get_rect(text=f"ZOOM {self.zoom * 100:.0f}", size=ZOOM_SIZE)
        self.text_manager.text[3].formating = self.zoom * 100
        self.text_manager.text[3].rect.topright = ZOOM_topright

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
        if not self.crushed and value > 0:
            self.points_size = POINTS_SIZE + POINTS_INCREASE
        # print('increasing')
        self.text_manager.text[5].rect = self.font.get_rect(text=f"{self.points:.0f}", size=self.points_size)
        self.text_manager.text[5].formating = self.points
        self.text_manager.text[5].rect.center = POINTS_center

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        if round(value - self._distance) >= 1:
            # print('true')
            self.points += round(value - self._distance)
            self._distance = value

    @property
    def pluspoints(self):
        return self._pluspoints

    @pluspoints.setter
    def pluspoints(self, value):
        if value > 0:
            self.pluspoints_counter = 255
        else:
            self.points += self._pluspoints
        self._pluspoints = value
        self.text_manager.text[6].rect = self.font.get_rect(text=f"+{self._pluspoints:.0f}", size=PLUSPOINTS_SIZE)
        self.text_manager.text[6].formating = self._pluspoints
        self.text_manager.text[6].rect.topleft = Vec(*self.text_manager.text[5].rect.topright) + (0, 20)

    @property
    def pluspoints_counter(self) -> int:
        return self._pluspoints_counter

    @pluspoints_counter.setter
    def pluspoints_counter(self, value):
        if value <= 0:
            self.pluspoints = 0
        self._pluspoints_counter = value

    @property
    def airtime(self):
        return self._airtime

    @airtime.setter
    def airtime(self, value):
        self._airtime = value
        self.text_manager.text[7].rect = self.font.get_rect(text=f"Air Time {self._airtime}", size=AT_SIZE)
        self.text_manager.text[7].formating = self._airtime
        self.text_manager.text[7].rect.topright = AT_topright

    def reset_variables(self):
        self.delta_zoom = self.airtime = self.pluspoints = self.points = self._pluspoints_counter = self._distance = \
            self._flips = self.coins_collected = self.camera_shake = self.go_counter = self.lasty = 0
        self.zoom = ZOOM
        self.points_size = POINTS_SIZE
        self.crushed = False
        self.scroll = Vec(0, 0)
        self.camera.reset()

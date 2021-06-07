import pygame as pg
import pygame.freetype as pg_ft
import pymunk as pk
from pymunk import Vec2d as Vec
import pymunk.pygame_util
from settings import *
from wheel import BackWheel, FrontWheel
from floors_manager import FloorsManager
from coinmanager import CoinManager
from background import Background
# from foreground import Foreground
from board import Board
from coin import Coin, SimpleCoin
from sprite import SpriteGroup
from screens import StartScreen, GoScreen
from functions import scale
from random import randint
import matplotlib.pylab as plt

var = []
var2 = []
var3 = []


class GameProperties:
    playing = running = waiting = True
    _crushed = False

    _coins_collected = _flips = _points = _pluspoints = _pluspoints_counter = _distance = _airtime = _lasty =\
        go_counter = delta_zoom = camera_shake = 0

    _zoom = ZOOM
    points_size = POINTS_SIZE
    displacement = DISPLACEMENT

    camera = Vec(0, 0)
    camera_focus = Vec(*CAMERA_INITIAL_POSITION)
    scroll = Vec(0, 0)

    f_rects = []

    simple_coin = SimpleCoin

    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.loading_screen = pg.image.load(LOADING_IMAGE)
        self.screen.blit(self.loading_screen, (0, 0))
        pg.display.flip()
        pg.Surface.set_colorkey(self.screen, (255, 255, 255))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(ICON))

        self.font = pg_ft.Font(JOYSTIX)
        self.start_fonts()

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
        # self.f_rects[1] = self.font.get_rect(text=f"Coins Collected {self.coins_collected}", size=CC_SIZE)
        self.f_rects[1] = self.font.get_rect(text=f"{self.coins_collected}", size=CC_SIZE)
        self.f_rects[1].topright = CC_topright
        self.simple_coin.rect.right = self.f_rects[1].left - 30
        self.simple_coin.rect.centery = self.f_rects[1].centery

    @property
    def flips(self):
        return self._flips

    @flips.setter
    def flips(self, value):
        self.pluspoints += value - self._flips
        self._flips = value
        self.f_rects[2] = self.font.get_rect(text=f"FLIPS {self.flips}", size=FLIPS_SIZE)
        self.f_rects[2].topright = FLIPS_topright

    @property
    def crushed(self):
        return self._crushed

    @crushed.setter
    def crushed(self, value):
        self._crushed = value
        # if value is True:
        #     self.camera_focus = self.board.body.position

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.displacement = self.camera_focus * (1 - self._zoom)
        self.f_rects[3] = self.font.get_rect(text=f"ZOOM {self.zoom * 100:.0f}", size=ZOOM_SIZE)
        self.f_rects[3].topright = ZOOM_topright

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
        if not self.crushed and value > 0:
            self.points_size = POINTS_SIZE + POINTS_INCREASE
        # print('increasing')
        self.f_rects[5] = self.font.get_rect(text=f"{self.points:.0f}", size=self.points_size)
        self.f_rects[5].center = POINTS_center

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
        if 0 > self.pluspoints_counter < 10 or self.crushed:
            self.points += self._pluspoints
            self._pluspoints = 0
            self.pluspoints_counter = 0
        return self._pluspoints

    @pluspoints.setter
    def pluspoints(self, value):
        if value > 0:
            self.pluspoints_counter = 255
        self._pluspoints = value
        self.f_rects[6] = self.font.get_rect(text=f"+{self._pluspoints:.0f}", size=PLUSPOINTS_SIZE)
        self.f_rects[6].topleft = Vec(*self.f_rects[5].topright) + (0, 20)

    @property
    def pluspoints_counter(self):
        return self._pluspoints_counter

    @pluspoints_counter.setter
    def pluspoints_counter(self, value):
        self._pluspoints_counter = value

    @property
    def airtime(self):
        return self._airtime

    @airtime.setter
    def airtime(self, value):
        self._airtime = value
        self.f_rects[7] = self.font.get_rect(text=f"Air Time {self._airtime}", size=AT_SIZE)
        self.f_rects[7].topright = AT_topright

    def start_fonts(self):
        self.f_rects = [
            self.font.get_rect(text=f"fps 60.00", size=FPS_SIZE),
            self.font.get_rect(text=f"0", size=CC_SIZE),
            self.font.get_rect(text=f"FLIPS 0", size=FLIPS_SIZE),
            self.font.get_rect(text=f"ZOOM {ZOOM*100:.0f}", size=ZOOM_SIZE),
            self.font.get_rect(text=f"Use the SPACE BAR to accelerate and press ESC to restart", size=RULES_SIZE),
            self.font.get_rect(text=f"0", size=self.points_size),
            self.font.get_rect(text=f"+0", size=PLUSPOINTS_SIZE),
            self.font.get_rect(text=f"Air Time 0", size=AT_SIZE),
        ]
        self.f_rects[0].topleft = FPS_topleft
        self.f_rects[1].topright = CC_topright
        self.f_rects[2].topright = FLIPS_topright
        self.f_rects[3].topright = ZOOM_topright
        self.f_rects[4].bottomleft = RULES_bottomleft
        self.f_rects[5].center = POINTS_center
        self.f_rects[6].topleft = Vec(*self.f_rects[5].topright) + (20, 0)
        self.f_rects[7].topright = AT_topright


class Game(GameProperties):
    def __init__(self):
        super().__init__()

        self.textures = {'ground': pg.image.load(TEXTURES.GROUND).convert(),
                         'grass': pg.image.load(TEXTURES.GRASS).convert()}
        self.textures['ground'].set_colorkey((255, 255, 255))
        self.textures['grass'].set_colorkey((255, 255, 255))

        self.draw_options = pk.pygame_util.DrawOptions(self.screen)
        self.clock = pg.time.Clock()
        self.space = pk.Space()
        self.backwheel = BackWheel(self)
        self.frontwheel = FrontWheel(self)
        self.board = Board(self, self.backwheel, self.frontwheel)
        self.floors = FloorsManager(self)
        self.coin_manager = CoinManager(self, period=1.5)
        self.background = Background(self)
        self.simple_coin = SimpleCoin(self, self.f_rects[1].topleft)
        # self.foreground = Foreground(self)
        self.all_sprites = SpriteGroup()
        self.all_sprites.add(self.background, self.floors, self.coin_manager, self.simple_coin, self.backwheel,
                             self.frontwheel, self.board)  # ,self.foreground)
        self.start_screen = StartScreen(self.font)
        self.go_screen = GoScreen(self.font, self.coins_collected, self.flips, self.points)

        # self.mouse_coins = []

    def new(self):
        # Start a new game
        self.delta_zoom = self.airtime = self.points = self.pluspoints = self._pluspoints_counter = self._distance = \
            self.flips = self.coins_collected = self.camera_shake = self.go_counter = 0
        self.zoom = ZOOM
        self.lasty = 0
        self.points_size = POINTS_SIZE
        self.crushed = False
        self.space = pk.Space()  # Create Pymunk Space
        self.space.gravity = GRAVITY  # Establish Gravity in Pymunk Space
        # self.camera_focus = Vec(*CAMERA_INITIAL_POSITION)
        self.scroll = Vec(0, 0)
        self.camera = Vec(0, 0)
        self.camera = Vec(0, 0)
        self.all_sprites.reset()
        # TODO: create a cool foreground
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            # if self.clock.get_time() % 4 == 0:
            self.events()
            self.draw()
            self.update()
            self.clock.tick(FPS)

    def update(self):
        # Game Loop - Update
        # print(self.airtime)
        # print(self.crushed)
        if self.airtime:
            self.airtime += 1
        self.space.step(0.5)
        self.space.step(0.5)
        self.all_sprites.update()
        if not self.crushed:
            scroll = scale(self.board.image, BOARD.DIMENSIONS, self.zoom).get_rect().center + \
                     self.board.body.position * self.zoom - self.scroll - self.camera_focus * self.zoom
            self.scroll += (scroll.x/SCROLL_DIVIDER[0], scroll.y/SCROLL_DIVIDER[1])
            self.distance = abs(self.backwheel.body.position.x/5000)
            # TODO: add smooth zooming when going at high speeds
            # distance = abs(self.backwheel.body.position.y - self.lasty)
            # if distance > 100:
            #     self.zoom = max(self.zoom - ZOOM_MIN, self.zoom - ZOOM_DECAY)
            # else:
            #     self.zoom = min(ZOOM, self.zoom + ZOOM_INCREASE)
            pass
        elif self.go_counter < 100:
            # TODO: fix bugs on the death cam, it doesn´t put the bike on the centre
            self.zoom += 0.003
            self.scroll += (scale(self.board.image, BOARD.DIMENSIONS, self.zoom).get_rect().center +
                            self.board.body.position * self.zoom - self.scroll - self.camera_focus * self.zoom)
            self.go_counter += 1
        else:
            self.playing = False
        self.camera = Vec(*self.scroll)
        if self.camera_shake:
            self.camera_shake -= 1
            self.camera += Vec(randint(-SHAKE, SHAKE), randint(-SHAKE, SHAKE))
        if self.pluspoints_counter:
            self.pluspoints_counter -= 3
            # print(self.pluspoints_counter)
        if self.points_size > POINTS_SIZE:
            self.points_size -= 1
        var.append(self.lasty)
        # var.append(self.backwheel.body.velocity.y)
        # var2.append(self.zoom)
        # var3.append(self.last_vel)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
                self.waiting = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.crushed = True
                if event.key == pg.K_SPACE and self.waiting:
                    self.waiting = False
                if event.key == pg.K_r:
                    pass
                # if event.key == pg.K_UP:
                #     self.zoom += 0.005
                # if event.key == pg.K_DOWN:
                #     self.zoom -= 0.005
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed(3)[0] and self.waiting:
                    self.waiting = False
                # print(pg.mouse.get_pos())
                    # self.mouse_coins.append(pg.mouse.get_pos())
        keys = pg.key.get_pressed()
        if not self.crushed:
            if keys[pg.K_SPACE] or pg.mouse.get_pressed(3)[0]:
                self.backwheel.body.angular_velocity += self.backwheel.thetaacc
                if self.board.checkground > 0:
                    self.board.checkground += 1
                    if self.board.checkground > 10:
                        self.board.body.angular_velocity -= self.board.thetaacc
            else:
                self.board.checkground = max(1, self.board.checkground - 1)
        if keys[pg.K_d]:
            # self.camera += Vec(40, 0)
            self.camera_shake = 8
        if keys[pg.K_a]:
            self.camera += Vec(-40, 0)
        if keys[pg.K_w]:
            self.camera += Vec(0, -40)
        if keys[pg.K_s]:
            self.camera += Vec(0, 40)
        if keys[pg.K_UP]:
            self.zoom += 0.005
        if keys[pg.K_DOWN]:
            self.zoom -= 0.005

    def draw(self):
        self.screen.fill(WHITE)
        if DEBUG:
            self.space.debug_draw(self.draw_options)
        else:
            self.all_sprites.draw()
        self.screen.blit(self.font.render(
            text=f"fps {float(self.clock.get_fps().__str__()):.2f}",
            fgcolor=GREY,
            size=FPS_SIZE)[0], self.f_rects[0])
        # self.screen.blit(self.font.render(
        #     text=f"Coins Collected {self.coins_collected}",
        #     fgcolor=BLACK,
        #     size=CC_SIZE)[0], self.f_rects[1])
        self.screen.blit(self.font.render(
            text=f"{self.coins_collected}",
            fgcolor=BLACK,
            size=CC_SIZE)[0], self.f_rects[1])
        # self.screen.blit(self.font.render(
        #     text=f"FLIPS {self.flips}",
        #     fgcolor=BLACK,
        #     size=FLIPS_SIZE)[0], self.f_rects[2])
        self.screen.blit(self.font.render(
            text=f"Air Time {self.airtime}",
            fgcolor=BLACK,
            size=AT_SIZE)[0], self.f_rects[7])
        # self.screen.blit(self.font.render(
        #     text=f"DISTANCE {self.distance}",
        #     fgcolor=BLACK,
        #     size=FLIPS_SIZE)[0], (40, 40))
        self.screen.blit(self.font.render(
            text=f"ZOOM {self.zoom*100:.0f}",
            fgcolor=BLACK,
            size=ZOOM_SIZE)[0], self.f_rects[3])
        self.screen.blit(self.font.render(
            text=f"Use the SPACE BAR to accelerate and press ESC to restart",
            fgcolor=BLACK,
            size=RULES_SIZE)[0], self.f_rects[4])
        self.screen.blit(self.font.render(
            text=f"{self.points:.0f}",
            fgcolor=BLACK,
            size=self.points_size)[0], self.f_rects[5])
        self.screen.blit(self.font.render(
            text=f"+{self.pluspoints:.0f}",
            fgcolor=[0, 0, 0, self.pluspoints_counter],
            size=PLUSPOINTS_SIZE)[0], self.f_rects[6])
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.waiting = True
        self.coin_manager.reset(ss=True)
        self.coin_manager.coins = [Coin(self, position=Vec(x, y), phase=i - (COIN.IDLE_ANIM_SIZE - 1) *
                                        (i // (COIN.IDLE_ANIM_SIZE - 1))) for i, (x, y) in enumerate(COIN.SS_POSITIONS)]
        while self.waiting:
            self.events()
            self.screen.fill(WHITE)
            self.start_screen.update()
            self.coin_manager.update()
            self.start_screen.draw(self.screen)
            self.coin_manager.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        # print(self.mouse_coins)
        pass

    def show_go_screen(self):
        # GO animation
        self.waiting = True
        self.go_screen = GoScreen(self.font, self.coins_collected, self.flips, self.points)
        while self.waiting and self.running:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.all_sprites.draw()
            self.go_screen.update()
            self.go_screen.draw(self.screen)
            pg.display.flip()

    def coin_collected(self, arbiter: pk.arbiter.Arbiter, space: pk.Space, data: dict):
        for shape in arbiter.shapes:
            shape: pymunk.Shape
            if hasattr(shape, 'activated'):
                shape.activated = False
                self.coins_collected += 1
        return True


if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()

    fig, ax = plt.subplots(3, 1)
    ax[0].plot(var)
    ax[0].set_title('lasty')
    # ax[1].plot(var2)
    # ax[1].set_title('zoom')
    # ax[2].set_title('deltavel')
    # ax[2].plot(var3)
    # plt.show()

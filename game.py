import pygame as pg
import pygame.freetype as pg_ft
import pymunk as pk
from pymunk import Vec2d as Vec
import pymunk.pygame_util
from settings import *
from settings.TEXT import *
from Managers import *
from Player import BackWheel, FrontWheel, Board
from Sprites import SpriteGroup, Background, SimpleCoin
from Utilities import Camera, Physics
import matplotlib.pylab as plt
# from math import sin
from gameproperties import GameProperties

var = []
var2 = []
var3 = []


class Game(GameProperties):
    def __init__(self):
        super().__init__()
        self.initialize_pygame()

        self.texture_manager = TextureManager()
        self.texture_manager.add()

        self.texture_manager.add(('ground', TEXTURES.GROUND), ('grass', TEXTURES.GRASS))

        self.data_manager = JsonManager(DATA)
        self.data = self.data_manager.load()

        self.font = pg_ft.Font(JOYSTIX)
        self.text_manager = TextManager(self.font)
        self.text_manager.bulk_adding(*TEXT)
        self.text_manager.set_text_update(self.text_update)

        self.camera = Camera(self, CAMERA_FOCUS)

        self.draw_options = pk.pygame_util.DrawOptions(self.screen)
        self.physics = Physics(self)
        self.physics.start_space(gravity=GRAVITY)

        self.initialize_sprites()
        self.screens_manager = ScreensManager(self)

    def initialize_sprites(self):
        # TODO: create a cool foreground
        # self.foreground = Foreground(self)
        self.backwheel = BackWheel(self, self.physics, costume=self.data['costumes']['backwheel'])
        self.frontwheel = FrontWheel(self, self.physics, costume=self.data['costumes']['frontwheel'])
        # print(self.data['costumes']['board'])
        self.board = Board(self, self.physics, self.backwheel, self.frontwheel, costume=self.data['costumes']['board'])
        self.floors_manager = FloorsManager(self, self.physics)
        self.coin_manager = CoinManager(self, self.physics, period=1.5)
        self.background = Background(self)
        self.simple_coin = SimpleCoin(self, self.text_manager.text[1].rect.topleft,
                                      images=self.coin_manager.idle_images)

        self.all_sprites = SpriteGroup()
        self.all_sprites.add(self.background, self.floors_manager, self.coin_manager, self.simple_coin, self.backwheel,
                             self.frontwheel, self.board)  # ,self.foreground)
        # self.mouse_coins = []

    def initialize_pygame(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.loading_screen = pg.image.load(LOADING_IMAGE)
        self.screen.blit(self.loading_screen, (0, 0))
        pg.display.flip()
        pg.Surface.set_colorkey(self.screen, (255, 255, 255))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(ICON))

        self.clock = pg.time.Clock()

    def start(self):
        self.screens_manager.run()

    def new(self):
        # Start a new game
        self.physics.reset()
        self.reset_variables()
        self.all_sprites.reset()

    def update(self):
        # Game Loop - Update
        if self.airtime:
            self.airtime += 1
        self.physics.update()
        self.all_sprites.update()
        self.camera.update()
        self.update_fonts()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.update_data()
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.crushed = True
                if event.key == pg.K_SPACE and self.waiting:
                    self.waiting = False
                    self.screens_manager.current_screen = 'playing'
                if event.key == pg.K_m and self.waiting:
                    self.waiting = False
                    self.screens_manager.current_screen = 'start'
                if event.key == pg.K_o:
                    self.backwheel.change_costume_to(self.backwheel.next_costume())
                    self.frontwheel.change_costume_to(self.frontwheel.next_costume())
                if event.key == pg.K_p:
                    self.board.change_costume_to(self.board.next_costume())
            if event.type == pg.MOUSEBUTTONDOWN:
                captured = self.all_sprites.mouseclick(pg.mouse.get_pos())
                if pg.mouse.get_pressed(3)[0] and self.waiting and not captured:
                    self.waiting = False
        self.check_keys()

    def check_keys(self, ):
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
                pass
        if keys[pg.K_d]:
            self.camera.shake = 8
        if keys[pg.K_a]:
            self.camera.position += Vec(-40, 0)
        if keys[pg.K_w]:
            self.camera.position += Vec(0, -40)
        if keys[pg.K_s]:
            self.camera.position += Vec(0, 40)
        if keys[pg.K_UP]:
            self.zoom += 0.005
        if keys[pg.K_DOWN]:
            self.zoom -= 0.005

    def text_update(self):
        self.text_manager.text[5].size = self.points_size
        self.text_manager.text[6].color = (*self.text_manager.text[6].color[:3], self.pluspoints_counter)
        self.text_manager.text[0].formating = self.clock.get_fps()

    def draw(self):
        self.screen.fill(WHITE)
        if DEBUG:
            self.physics.space.debug_draw(self.draw_options)
        else:
            self.all_sprites.draw()

        self.text_manager.update()
        # self.texts[9][5] = self.board.checkground
        self.text_manager.draw(self.screen)
        pg.display.flip()

    def update_fonts(self):
        if self.pluspoints_counter:
            self.pluspoints_counter: int = max(0, self.pluspoints_counter - 4)
        if self.points_size > POINTS_SIZE:
            self.points_size -= 1

    def update_data(self):
        self.data_manager.update(self.data)
        return True

    @staticmethod
    def quit():
        pg.quit()


if __name__ == '__main__':
    fig, ax = plt.subplots(3, 1)
    ax[0].plot(var)
    ax[0].set_title('lasty')
    ax[1].plot(var2)
    ax[1].set_title('zoom')
    ax[2].set_title('deltavel')
    ax[2].plot(var3)
    plt.show()

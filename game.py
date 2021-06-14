import pygame as pg
import pygame.freetype as pg_ft
import pymunk as pk
from pymunk import Vec2d as Vec
import pymunk.pygame_util
from settings import *
from settings.TEXT import *
from Managers import *
from Sprites import *
from Utilities import *
import matplotlib.pylab as plt
# from math import sin
from gameproperties import GameProperties

var = []
var2 = []
var3 = []


# TODO: Continue refactoring this
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
        self.initialize_screens()

    def initialize_screens(self):
        self.start_screen = StartScreen(self)
        self.store_screen = StoreScreen(self)
        self.go_screen = GoScreen(self)

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

    def new(self):
        # Start a new game
        self.physics.reset()
        self.reset_variables()
        self.all_sprites.reset()
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
        self.update_data()

    def update(self):
        # Game Loop - Update
        # print(self.airtime)
        # print(self.crushed)
        # TODO:  fix zooming
        # self.zoom -= sin(pg.time.get_ticks()*.006)*0.01
        if self.airtime:
            self.airtime += 1
        self.physics.update()
        self.all_sprites.update()
        self.camera.update()
        self.update_fonts()
        # var.append(self.lasty)
        # var.append(self.backwheel.body.velocity.y)
        # var2.append(self.zoom)
        # var3.append(self.last_vel)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.update_data()
                self.running = False
                self.playing = False
                self.waiting = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.crushed = True
                if event.key == pg.K_SPACE and self.waiting:
                    self.change_screen_to('game')
                if event.key == pg.K_m and self.waiting:
                    self.change_screen_to('menu')
                if event.key == pg.K_o:
                    self.backwheel.change_costume_to(self.backwheel.next_costume())
                    self.frontwheel.change_costume_to(self.frontwheel.next_costume())
                if event.key == pg.K_p:
                    self.board.change_costume_to(self.board.next_costume())
            if event.type == pg.MOUSEBUTTONDOWN:
                captured = self.all_sprites.mouseclick(pg.mouse.get_pos())
                if pg.mouse.get_pressed(3)[0] and self.waiting and not captured and self.current_screen != 'store':
                    self.waiting = False
        self.check_keys()

    def change_screen_to(self, screen: str):
        self.waiting = False
        self.current_screen = screen

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

    def show_store(self):
        self.store_screen.reset()
        self.waiting = True
        self.coin_manager.reset(ss=True)
        self.all_sprites.add(self.store_screen)
        while self.waiting:
            self.events()
            self.screen.fill(WHITE)
            self.store_screen.update()
            self.store_screen.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        self.all_sprites.remove(self.store_screen)
        if self.current_screen == 'menu':
            self.show_menu()
        # print(self.mouse_coins)
        pass

    def show_start_screen(self):
        # game splash/start screen
        self.start_screen.reset()
        self.waiting = True
        self.coin_manager.reset(ss=True)
        self.all_sprites.add(self.start_screen)
        self.coin_manager.coins = [Coin(self, position=Vec(x, y), phase=i - (COIN.IDLE_ANIM_SIZE - 1) *
                                        (i // (COIN.IDLE_ANIM_SIZE - 1))) for i, (x, y) in enumerate(COIN.SS_POSITIONS)]
        while self.waiting:
            self.events()
            self.screen.fill(WHITE)
            self.start_screen.update()
            self.coin_manager.update()
            self.start_screen.draw()
            self.coin_manager.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        self.all_sprites.remove(self.start_screen)
        if self.current_screen == 'store':
            self.show_store()
        # print(self.mouse_coins)
        pass

    def show_menu(self):
        # game splash/start screen
        self.show_start_screen()

    def show_go_screen(self):
        # GO animation
        self.waiting = True
        self.go_screen = GoScreen(self)
        while self.waiting and self.running:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.all_sprites.draw()
            self.go_screen.update()
            self.go_screen.draw(self.screen)
            pg.display.flip()
        if self.current_screen == 'menu':
            self.show_menu()

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

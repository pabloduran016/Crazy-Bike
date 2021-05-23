import pygame as pg
import pygame.freetype as pg_ft
import pymunk as pk
import pymunk.pygame_util
from settings import *
from wheel import Wheel
from floors_manager import FloorsManager
from coinmanager import CoinManager
from background import Background
from foreground import Foreground
from board import Board
from coin import Coin
from sprite import SpriteGroup
from screens import StartScreen, GoScreen
vec = pk.Vec2d


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.Surface.set_colorkey(self.screen, (255, 255, 255))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(ICON))
        self.draw_options = pk.pygame_util.DrawOptions(self.screen)
        self.clock = pg.time.Clock()
        self.playing = True
        self.running = True
        self.waiting = True
        self.zoom = ZOOM
        self.displacement = DISPLACEMENT
        self.space = pk.Space()
        self.backwheel = Wheel(self, 'backwheel')
        self.frontwheel = Wheel(self, 'backwheel')
        self.board = Board(self, self.backwheel, self.frontwheel)
        self.floors = FloorsManager(self)
        self.coin_manager = CoinManager(self, 8)
        self.background = Background(self)
        self.foreground = Foreground(self)
        self.all_sprites = SpriteGroup()
        self.crushed = False
        self.camera = vec(0, 0)
        self.camera_initial_position = vec(*CAMERA_INITIAL_POSITION)
        self.font = pg_ft.Font(ARCADECLASSIC)
        self.coins_collected = 0
        self.flips = 0
        self.f_rects = []
        self.update_fonts()
        self.start_screen = StartScreen(self.font)
        self.go_screen = GoScreen(self.font, self.coins_collected, self.flips)
        self.textures = {'ground': pg.image.load(TEXTURES.GROUND).convert(),
                         'grass': pg.image.load(TEXTURES.GRASS).convert()}
        self.textures['ground'].set_colorkey((255, 255, 255))
        self.textures['grass'].set_colorkey((255, 255, 255))
        self.camera_counter = 0
        # self.mouse_coins = []

    def new(self):
        # Start a new game
        self.space = pk.Space()  # Create Pymunk Space
        self.space.gravity = GRAVITY  # Establish Gravity in Pymunk Space
        self.coins_collected = 0
        self.camera = vec(0, 0)
        self.crushed = False
        self.camera_counter = 0
        self.flips = 0
        self.all_sprites = SpriteGroup()
        self.backwheel = Wheel(self, 'backwheel')  # Create a Backwheel object add it to Pymunk Space
        self.frontwheel = Wheel(self, 'frontwheel')  # Create a Frontwheel object add it to Pymunk Space
        self.board = Board(self, self.backwheel, self.frontwheel)  # Create Board and connect both wheels
        self.floors = FloorsManager(self)
        self.coin_manager = CoinManager(self, period=8)
        self.background = Background(self)
        self.background = Background(self)
        self.all_sprites.add(self.background, self.floors, self.coin_manager, self.backwheel, self.frontwheel,
                             self.board, self.foreground)
        self.all_sprites.start()
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

    def update(self):
        # Game Loop - Update
        self.space.step(0.5)
        self.space.step(0.5)
        self.all_sprites.update()
        if not self.crushed:
            self.camera += (pg.transform.scale(self.board.image,
                                               (round(BOARD.DIMENSIONS[0]*self.zoom),
                                                round(BOARD.DIMENSIONS[1]*self.zoom))).get_rect().center +
                            self.board.body.position*self.zoom - self.camera - self.camera_initial_position*self.zoom)/3
            pass
        elif self.camera_counter < 20:
            self.camera += (-10, 0)
            self.camera_counter += 1
        else:
            self.playing = False
        self.update_fonts()

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
                if event.key == pg.K_SPACE and self.waiting:
                    self.waiting = False
                if event.key == pg.K_r:
                    self.backwheel.reset()
                    self.frontwheel.reset()
                    self.board.reset()
                if event.key == pg.K_UP:
                    self.zoom += 0.005
                    self.displacement = self.camera_initial_position*(1-self.zoom)
                    self.camera += (pg.transform.scale(self.board.image,
                                    (round(BOARD.DIMENSIONS[0] * self.zoom),
                                     round(BOARD.DIMENSIONS[1] * self.zoom))).get_rect().center +
                                    self.board.body.position * self.zoom - self.camera - self.camera_initial_position *
                                    self.zoom) / 3
                if event.key == pg.K_DOWN:
                    self.zoom -= 0.005
                    self.displacement = self.camera_initial_position*(1-self.zoom)
                    self.camera += (pg.transform.scale(self.board.image,
                                                       (round(BOARD.DIMENSIONS[0] * self.zoom),
                                                        round(BOARD.DIMENSIONS[1] * self.zoom))).get_rect().center +
                                    self.board.body.position * self.zoom - self.camera - self.camera_initial_position *
                                    self.zoom)
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed(3)[0] and self.waiting:
                    self.waiting = False
                    # self.mouse_coins.append(pg.mouse.get_pos())
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] or pg.mouse.get_pressed(3)[0]:
            self.backwheel.body.angular_velocity += self.backwheel.thetaacc
            if self.board.checkground > 0:
                self.board.checkground += 1
                if self.board.checkground > 10:
                    self.board.body.angular_velocity -= self.board.thetaacc
        else:
            self.board.checkground = max(1, self.board.checkground - 1)
        if keys[pg.K_d]:
            self.camera += vec(40, 0)
        if keys[pg.K_a]:
            self.camera += vec(-40, 0)
        if keys[pg.K_w]:
            self.camera += vec(0, -40)
        if keys[pg.K_s]:
            self.camera += vec(0, 40)

    def draw(self):
        self.screen.fill(WHITE)
        if DEBUG:
            self.space.debug_draw(self.draw_options)
        else:
            self.all_sprites.draw()
        self.screen.blit(self.font.render(
            text=f"fps    {self.clock.get_fps():.0f}",
            fgcolor=GREY,
            size=30)[0], self.f_rects[0])
        self.screen.blit(self.font.render(
            text=f"Coins Collected      {self.coins_collected}",
            fgcolor=BLACK,
            size=30)[0], self.f_rects[1])
        self.screen.blit(self.font.render(
            text=f"FLIPS      {self.flips}",
            fgcolor=BLACK,
            size=30)[0], self.f_rects[2])
        # self.screen.blit(self.font.render(
        #     text=f"ZOOM      {self.zoom:.2f}",
        #     fgcolor=BLACK,
        #     size=30)[0], self.f_rects[3])
        self.screen.blit(self.font.render(
            text="Use    the    SPACE    BAR    to    accelerate    and    press    ESC    to    restart",
            fgcolor=BLACK,
            size=25)[0], self.f_rects[4])
        # self.screen.blit(self.font.render
        #                  (f"Check Ground: {self.board.checkground}", True, BLACK),
        #                  (WIDTH - 200, 40))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.waiting = True
        self.coin_manager = CoinManager(self, ss=True)
        self.coin_manager.coins = [Coin(self, vec(x, y), i - (COIN.IDLE_ANIM_SIZE - 1) *
                                        (i // (COIN.IDLE_ANIM_SIZE - 1))) for i, (x, y) in enumerate(COIN.SS_POSITIONS)]
        while self.waiting:
            self.clock.tick(FPS)
            self.events()
            self.screen.fill(WHITE)
            self.start_screen.update()
            self.coin_manager.update()
            self.start_screen.draw(self.screen)
            self.coin_manager.draw()
            pg.display.flip()
        # print(self.mouse_coins)
        pass

    def show_go_screen(self):
        # GO animation
        self.waiting = True
        self.go_screen = GoScreen(self.font, self.coins_collected, self.flips)
        while self.waiting and self.running:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.all_sprites.draw()
            self.go_screen.update()
            self.go_screen.draw(self.screen)
            pg.display.flip()

    def update_fonts(self):
        self.f_rects = [
            self.font.get_rect(text=f"fps       " + str(self.clock.get_fps().__str__()), size=30),
            self.font.get_rect(text=f"Coins Collected      {self.coins_collected}", size=30),
            self.font.get_rect(text=f"FLIPS      {self.flips}", size=30),
            self.font.get_rect(text=f"ZOOM      {self.zoom:.2f}", size=30),
            self.font.get_rect(text=f"Use    the    SPACE    BAR    to    accelerate    and    press    ESC    to    "
                                    f"restart", size=25),
        ]
        self.f_rects[0].topleft = F1_topleft
        self.f_rects[1].topright = F2_topright
        self.f_rects[2].topright = F3_topright
        self.f_rects[3].topright = F4_topright
        self.f_rects[4].bottomleft = F5_bottomleft

    def coin_collected(self, arbiter, space, data):
        """
        :type arbiter: pymunk.arbiter.Arbiter
        :type space: pymunk.space.Space
        :type data: dict
        """
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

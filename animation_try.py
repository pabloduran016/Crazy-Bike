import pygame as pg
import pygame.freetype as pg_ft
from settings.colors import *
from sprite import SpriteGroup

FPS = 60
DIMENSIONS = 480, 480
COIN_ANIM_SIZE = 60
COLLECTED_ANIM = 'Assets/Animations/Coin/Idle_4/'
IDLE_ANIM = 'Assets/Animations/Coin/Idle_4/'
JOYSTIX = 'Assets/Fonts/joystix monospace.ttf'


class Game:
    pg.init()
    screen = pg.display.set_mode((900, 900))
    clock = pg.time.Clock()
    running = playing = True
    _collected_anim = False
    sprites = SpriteGroup()
    font = pg_ft.Font(JOYSTIX)


    def __init__(self):
        self.coin = Coin(self)
        self.sprites.add(self.coin)

    @property
    def collected_anim(self):
        return self._collected_anim

    @collected_anim.setter
    def collected_anim(self, value):
        self._collected_anim = value

    def new(self):
        self.run()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.collected_anim = True

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        self.screen.blit(self.font.render(
            text=str(self.collected_anim),
            fgcolor=[0, 0, 0, 255],
            size=30)[0], (0, 0))
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


class Coin(pg.sprite.Sprite):
    def __init__(self, game: Game, period=2):
        super().__init__()
        self.game = game
        self.idle_images = [pg.image.load(IDLE_ANIM + f'{(x + 1):04}.png').convert_alpha()
                            for x in range(COIN_ANIM_SIZE)]
        self.collected_images = [pg.image.load(COLLECTED_ANIM + f'{(x + 1):04}.png').convert_alpha()
                            for x in range(COIN_ANIM_SIZE)]
        self.image = self.idle_images[0]
        self.rect = pg.Rect(0, 0, DIMENSIONS[0], DIMENSIONS[1])
        self.rect.center = (450, 450)
        self.idle_count = -0.5
        self.collected_count = 0
        self.period = period

    def update(self, *args, **kwargs) -> None:
        if type(self.game.collected_anim) == int:
            self.game.collected_anim += 1
            if self.game.collected_anim > 100:
                self.game.collected_anim = False
        elif self.game.collected_anim:
            self.collected_count += 10
            if self.collected_count > 200:
                self.collected_count = 0
                self.game.collected_anim = 1
        else:
            self.idle_count += 1 / self.period
            if round(self.idle_count) > COIN_ANIM_SIZE - 1:
                self.idle_count = 0

    def draw(self):
        if type(self.game.collected_anim) == int:
            pass
        elif self.game.collected_anim:
            width1 = (((self.collected_count+DIMENSIONS[0]/4)/100)*DIMENSIONS[0]/2)
            width2 = DIMENSIONS[0]/4 + DIMENSIONS[0]/2 - (self.collected_count/200)*(DIMENSIONS[0]/4 + DIMENSIONS[0]/2)
            width = max(width1, width2)
            self.image = pg.Surface((width*2, width*2), pg.SRCALPHA)
            self.image.set_colorkey((255, 255, 255))
            rect = self.image.get_rect()
            pg.draw.circle(self.image, YELLOW[:3] + (int(255-255*self.collected_count/200),), rect.center, width1)
            pg.draw.circle(self.image, WHITE[:3] + (int(255-255*self.collected_count/200),), rect.center, width2)
            rect.center = self.rect.center
            self.game.screen.blit(self.image, rect.topleft)
        else:
            self.image = self.idle_images[round(self.idle_count)]
            self.game.screen.blit(pg.transform.scale(self.image, DIMENSIONS), self.rect.topleft)


if __name__ == '__main__':
    g = Game()
    while g.playing:
        g.show_start_screen()
        g.new()
        g.show_go_screen()

    pg.quit()

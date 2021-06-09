from settings import STARTSCREEN, GOSCREEN
from settings.FONTS import *
from pygame.image import load
from settings.colors import *
from functions import formated


class StartScreen:
    def __init__(self, font):
        self.image = load(STARTSCREEN.IMAGE).convert_alpha()
        self.count = -.5
        self.font = font

        self.f1_rect = font.get_rect(text=f"CRAZY BIKE", size=STARTSCREEN.CB_SIZE)
        self.f1_rect.center = STARTSCREEN.CB_center

        self.f2_rect = font.get_rect(text="Press the SPACE BAR or right click to continue",
                                     size=STARTSCREEN.SPACE_SIZE)
        self.f2_rect.center = STARTSCREEN.SPACE_center

    def update(self):
        self.count += 1/20
        if round(self.count) > STARTSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5

        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        screen.blit(self.font.render(
            text=f"CRAZY BIKE",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=STARTSCREEN.CB_SIZE)[0], self.f1_rect.topleft)
        screen.blit(self.font.render(
            text="Press the SPACE BAR or right click to continue",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=STARTSCREEN.SPACE_SIZE)[0], self.f2_rect.topleft)


class GoScreen:
    def __init__(self, font, coins_collected, flips, points):
        self.count = -.5
        self.font = font
        self.coins_collected = coins_collected
        self.flips = flips
        self.points = points
        self.f_color = BLACK
        self.texts = [
            [font.get_rect(text=f"GAME OVER", size=GOSCREEN.GO_SIZE), f"GAME OVER", GREY, GOSCREEN.GO_SIZE, True, None],
            [font.get_rect(text=f"{self.coins_collected}", size=CC_SIZE), f"{self.coins_collected}", BLACK,
             CC_SIZE, True, None],
            [font.get_rect(text=f"FLIPS {self.flips}", size=FLIPS_SIZE), f"FLIPS {self.flips}", BLACK, FLIPS_SIZE,
             False, None],
            [font.get_rect(text=f"PRESS SPACE TO RESTART", size=GOSCREEN.SPACE_SIZE), f"PRESS SPACE TO RESTART",
              BLACK, GOSCREEN.SPACE_SIZE, True, None],
            [font.get_rect(text=f"PRESS M TO GO TO MENU", size=GOSCREEN.MENU_SIZE), f"PRESS M TO GO TO MENU",
              BLACK, GOSCREEN.MENU_SIZE, True, None],
            [font.get_rect(text=f"{self.points:.0f}", size=POINTS_SIZE), f"{self.points:.0f}", BLACK, POINTS_SIZE,
             True, None],
        ]
        self.texts[0][0].center = GOSCREEN.GO_center
        self.texts[1][0].topright = CC_topright
        self.texts[2][0].topright = FLIPS_topright
        self.texts[3][0].center = GOSCREEN.SPACE_center
        self.texts[4][0].center = GOSCREEN.MENU_center
        self.texts[5][0].center = POINTS_center

    def update(self):
        self.count += 1/20
        if round(self.count) > GOSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5
        pass

    def draw(self, screen):
        self.texts[0][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[3][2] = BLACK if round(self.count) == 0 else WHITE
        self.texts[4][2] = WHITE if round(self.count) == 0 else BLACK
        for rect, text, color, size, activated, value in self.texts:
            if activated:
                screen.blit(self.font.render(
                    text=formated(text, value),
                    fgcolor=color,
                    size=size)[0], rect)

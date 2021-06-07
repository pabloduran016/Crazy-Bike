from settings import STARTSCREEN, GOSCREEN, BLACK, WHITE
from settings.FONTS import *
from pygame.image import load


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
        self.f_rects = [
            font.get_rect(text=f"GAME OVER", size=GOSCREEN.GO_SIZE),
            font.get_rect(text=f"{self.coins_collected}", size=CC_SIZE),
            font.get_rect(text=f"FLIPS {self.flips}", size=FLIPS_SIZE),
            font.get_rect(text=f"PRESS SPACE TO CONTINUE", size=GOSCREEN.SPACE_SIZE),
            font.get_rect(text=f"{self.points:.0f}", size=POINTS_SIZE)
        ]
        self.f_rects[0].center = GOSCREEN.GO_center
        self.f_rects[1].topright = CC_topright
        self.f_rects[2].topright = FLIPS_topright
        self.f_rects[3].center = GOSCREEN.SPACE_center
        self.f_rects[4].center = POINTS_center

    def update(self):
        self.count += 1/20
        if round(self.count) > GOSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5
        pass

    def draw(self, screen):
        screen.blit(self.font.render(
            text=f"GAME OVER",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=GOSCREEN.GO_SIZE)[0], self.f_rects[0].topleft)
        screen.blit(self.font.render(
            text=f"{self.coins_collected}",
            fgcolor=BLACK,
            size=CC_SIZE)[0], self.f_rects[1].topleft)
        screen.blit(self.font.render(
            text=f"FLIPS {self.flips}",
            fgcolor=BLACK,
            size=FLIPS_SIZE)[0], self.f_rects[2].topleft)
        screen.blit(self.font.render(
            text="PRESS SPACE TO CONTINUE",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=GOSCREEN.SPACE_SIZE)[0], self.f_rects[3].topleft)
        screen.blit(self.font.render(
            text=f"{self.points:.0f}",
            fgcolor=BLACK,
            size=POINTS_SIZE)[0], self.f_rects[4])

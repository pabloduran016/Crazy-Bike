from settings import STARTSCREEN, GOSCREEN, BLACK, WHITE
from pygame.image import load


class StartScreen:
    def __init__(self, font):
        self.image = load(STARTSCREEN.IMAGE).convert_alpha()
        self.count = -.5
        self.font = font

        self.f1_rect = font.get_rect(text=f"CRAZY    BIKE", size=100)
        self.f1_rect.center = STARTSCREEN.F1_center

        self.f2_rect = font.get_rect(text="Press    the    SPACE    BAR    or    right    click    to    continue",
                                     size=30)
        self.f2_rect.center = STARTSCREEN.F2_center

    def update(self):
        self.count += 1/20
        if round(self.count) > STARTSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5

        assert round(self.count) == 0 or round(self.count) == 1, f'Expected count to be 1 or cero, got {self.count}'

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        screen.blit(self.font.render(
            text=f"CRAZY    BIKE",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=100)[0], self.f1_rect.topleft)
        screen.blit(self.font.render(
            text=f"Press    the    SPACE    BAR    or    right    click    to    continue",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=30)[0], self.f2_rect.topleft)


class GoScreen:
    def __init__(self, font, coins_collected, flips):
        self.count = -.5
        self.font = font
        self.coins_collected = coins_collected
        self.flips = flips
        self.f_color = BLACK
        self.f_rects = [
            font.get_rect(text=f"GAME    OVER", size=100),
            font.get_rect(text=f"Coins Collected      {self.coins_collected}", size=30),
            font.get_rect(text=f"FLIPS      {self.flips}", size=30),
            font.get_rect(text=f"PRESS    SPACE    TO    CONTINUE", size=60)
        ]
        self.f_rects[0].center = GOSCREEN.F1_center
        self.f_rects[1].topright = GOSCREEN.F2_topright
        self.f_rects[2].topright = GOSCREEN.F3_topright
        self.f_rects[3].center = GOSCREEN.F4_center

    def update(self):
        self.count += 1/20
        if round(self.count) > GOSCREEN.ANIMATION_SIZE - 1:
            self.count = -.5
        pass

    def draw(self, screen):
        screen.blit(self.font.render(
            text=f"GAME    OVER",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=100)[0], self.f_rects[0].topleft)
        screen.blit(self.font.render(
            text=f"Coins Collected      {self.coins_collected}",
            fgcolor=BLACK,
            size=30)[0], self.f_rects[1].topleft)
        screen.blit(self.font.render(
            text=f"FLIPS      {self.flips}",
            fgcolor=BLACK,
            size=30)[0], self.f_rects[2].topleft)
        screen.blit(self.font.render(
            text="PRESS    SPACE    TO    CONTINUE",
            fgcolor=BLACK if round(self.count) == 0 else WHITE,
            size=60)[0], self.f_rects[3].topleft)

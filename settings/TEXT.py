from .colors import *
from .GAME import WIDTH, HEIGHT


FPS_topleft = 20, 20
FPS_SIZE = 20
CC_topright = 880, 20
CC_SIZE = 20
FLIPS_topright = 880, 50
FLIPS_SIZE = 20
ZOOM_topright = 880, 80
ZOOM_SIZE = 20
RULES_bottomleft = 20, 880
RULES_SIZE = 15
POINTS_center = WIDTH/2, HEIGHT/5
POINTS_SIZE = 100
POINTS_INCREASE = 20
PLUSPOINTS_SIZE = 60
AT_topright = 880, 110
AT_SIZE = 20
HS_topcenter = 450, 20
HS_SIZE = 20

TEXT = (
        ("fps {:.2f}", GREY, FPS_SIZE, True, 0, {'topleft': (20, 20)}),
        ('{}', BLACK, CC_SIZE, True, None, {'topright': (880, 20)}),
        ("FLIPS {}", BLACK, FLIPS_SIZE, False, None, {'topright': (880, 50)}),
        ("ZOOM {:.0f}", BLACK, ZOOM_SIZE, True, None, {'topright': (880, 80)}),
        (f"Use the SPACE BAR to accelerate and press ESC to restart", BLACK, RULES_SIZE, True, None,
                {'bottomleft': (20, 880)}),
        ("{}", BLACK, POINTS_SIZE, True, None, {'center': (WIDTH/2, HEIGHT/5)}),
        ("+{:.0f}", BLACK, PLUSPOINTS_SIZE, True, None),
        ("Air Time {}", BLACK, AT_SIZE, False, None, {'topright': (880, 110)}),
        ("HIGH SCORE: {}", BLACK, HS_SIZE, True, None, {'top': 20, 'centerx': 450}),
        # [self.font.get_rect(text=f"Checkground: 0", size=HS_SIZE),
        #      "Checkground: {}", BLACK, HS_SIZE, True, None],
)

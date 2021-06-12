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
        ("fps {:.2f}", GREY, FPS_SIZE, True, 0),
        ('{}', BLACK, CC_SIZE, True, None),
        ("FLIPS {}", BLACK, FLIPS_SIZE, False, None),
        ("ZOOM {:.0f}", BLACK, ZOOM_SIZE, True, None),
        (f"Use the SPACE BAR to accelerate and press ESC to restart", BLACK, RULES_SIZE, True, None),
        ("{}", BLACK, POINTS_SIZE, True, None),
        ("+{:.0f}", BLACK, PLUSPOINTS_SIZE, True, None),
        ("Air Time {}", BLACK, AT_SIZE, False, None),
        ("HIGH SCORE: {}", BLACK, HS_SIZE, True, None),
        # [self.font.get_rect(text=f"Checkground: 0", size=HS_SIZE),
        #      "Checkground: {}", BLACK, HS_SIZE, True, None],
)
# self.texts[0][0].topleft = FPS_topleft
# self.texts[1][0].topright = CC_topright
# self.texts[2][0].topright = FLIPS_topright
# self.texts[3][0].topright = ZOOM_topright
# self.texts[4][0].bottomleft = RULES_bottomleft
# self.texts[5][0].center = POINTS_center
# self.texts[6][0].topleft = Vec(*self.texts[5][0].topright) + (20, 0)
# self.texts[7][0].topright = AT_topright
# self.texts[8][0].centerx, self.texts[8][0].top = HS_topcenter
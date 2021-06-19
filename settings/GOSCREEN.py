from .colors import *

ANIMATION = 'Assets/Animations/Start_Screen_anim/'
ANIMATION_SIZE = 2
GO_center = 450, 450
GO_SIZE = 70
SPACE_center = 450, 800
SPACE_SIZE = 20
MENU_center = 450, 840
MENU_SIZE = 20

TEXT = (
    ('GAME OVER', BLACK, 70, True, None, {'center': (450, 450)}),
    ('{}', BLACK, 20, True, None, {'topright': (880, 20)}),
    ('FLIPS {}', BLACK, 20, False, None, {'topright': (880, 50)}),
    ('PRESS SPACE TO RESTART', BLACK, 20, True, None, {'center': (450, 800)}),
    ('PRESS M TO GO TO MENU', BLACK, 20, True, None, {'center': (450, 840)}),
    ("{}", BLACK, 100, True, None, {'center': (450, 180)}),
    ("HIGH SCORE: {}", BLACK, 20, True, None, {'top': 20, 'centerx': 450}),
)

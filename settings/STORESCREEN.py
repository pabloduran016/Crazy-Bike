from .colors import *

IMAGE = 'Assets/Images/startscreen3.png'
ANIMATION_SIZE = 2
ITEM_DIMENSIONS = 200, 175
ITEM_IMAGE_DIMENSIONS = 50
ITEM_SPACING = (20, 15)
ITEM_INITIAL_POSITION = (0, 220)
ITEMS = [
    ['MOTORBIKE WHEELS', 15, (0, 0), 'Assets/Images/Player_costumes/motorbike_wheel.png', 400, 'wheel'],
    ['MOTORBIKE BOARD', 15, (1, 0), 'Assets/Images/Player_costumes/motorbike_board.png', 400, 'board'],
    ['BIKE WHEELS', 15, (2, 0), 'Assets/Images/Player_costumes/bike_wheel.png', 400, 'wheel'],
    ['BIKE BOARD', 15, (3, 0), 'Assets/Images/Player_costumes/bike_board.png', 400, 'board'],
    ['CAR WHEEL', 15, (1, 1), 'Assets/Images/Player_costumes/car_wheel.png', 400, 'wheel'],
    ['CAR BOARD', 15, (0, 1), 'Assets/Images/Player_costumes/car_board.png', 400, 'board'],
]

TEXT = (
    ('CRAZY BIKE', BLACK, 70, True, None, {'center': (450, 100)}),
    ('STORE', BLACK, 50, True, None, {'center': (450, 170)}),
    ('PRESS SPACE TO START', BLACK, 20, True, None, {'center': (450, 800)}),
    ('RESS M TO RETURN TO MENU', BLACK, 20, True, None, {'center': (450, 850)}),
    ('{}', BLACK, 20, True, 0, {'topright': (880, 20)}),
    ("HIGH SCORE: {}", BLACK, 20, True, None, {'top': 20, 'centerx': 450}),
    ("NOT ENOUGH COINS", RED, 20, True, None, {'center': (450, 700)}),
)
BACKWHEEL_POSITION = (225, 650)
WHEELS_DIMENSIONS = 40, 40
WHEELS_DISTANCE = 90 * WHEELS_DIMENSIONS[0]/40
BOARD_DIMENSIONS = 150, 200

STORE_BUTTON_SIZE = 80, 80
STORE_BUTTON_center = 830, 830
STORE_BUTTON_IMAGE = 'Assets/Images/store_button.png'

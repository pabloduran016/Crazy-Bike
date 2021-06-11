from .colors import BLACK
COLOR = BLACK
COSTUMES = {
    'motorbike': {'image': 'Assets/Images/Player_costumes/motorbike_board.png', 'dimensions': (120, 69), 'pivot': (20, 56)},
    'bike': {'image': 'Assets/Images/Player_costumes/bike_board.png', 'dimensions': (98, 66), 'pivot': (5, 56)},
    'car': {'image': 'Assets/Images/Player_costumes/car_board.png', 'dimensions': (160, 64), 'pivot': (34, 56)},
}
DENSITY = 0.1
VERICES = ((-5, -1),
           (30, -32),
           (23, -44),
           (41, -44),
           (82, -54),
           (92, -1))
FRICTION = 1
THETAACC = 0.07
ELASTICITY = 0
AIR_DRAG_MULTIPLIER = .5

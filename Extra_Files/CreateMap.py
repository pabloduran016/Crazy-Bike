from random import randint


class MapCreator:
    selection: int
    modes = ['up_parable', 'down_parable', 'sine', 'up_line', 'down_line']

    def __init__(self):
        pass

    @classmethod
    def select_type(cls):
        return cls.modes[randint(0, len(cls.modes)-1)]

    @classmethod
    def get_map(cls, initial_y):
        selection = cls.select_type()
        distance = randint(1200, 2000)
        values = []
        if selection == 'up_parable':
            for x in range(distance):
                a = 1
                value = a * x ** 2 + initial_y

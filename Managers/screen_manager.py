from Screens import StoreScreen, StartScreen, GoScreen
from settings import *


SCREENS = {'start, store, menu', 'playing'}


class ScreensManager:
    current_screen: str = 'start'

    def __init__(self, game):
        self.game = game
        self.start_screen = StartScreen(game)
        self.store_screen = StoreScreen(game)
        self.go_screen = GoScreen(game)

    def run(self):
        while self.game.running:
            self.change_screen_to(self.current_screen)

    def change_screen_to(self, screen: str):
        if hasattr(self, screen):
            screen_call = getattr(self, screen)
            if callable(screen_call):
                screen_call()
            else:
                raise ValueError(f'Screen {screen} is not valid')
        else:
            raise ValueError(f'Screen {screen} not known')

    def playing(self):
        # Game Loop
        self.game.playing = True
        self.game.new()
        while self.game.playing and self.game.running:
            # if self.clock.get_time() % 4 == 0:
            self.game.events()
            self.game.draw()
            self.game.update()
            self.game.clock.tick(FPS)
        self.current_screen = 'go'
        self.game.update_data()

    def go(self):
        # GO animation
        with self.go_screen:
            while self.game.waiting and self.game.running:
                self.go_screen.run()

    def store(self):
        with self.store_screen:
            while self.game.waiting and self.game.running:
                self.store_screen.run()

    def menu(self):
        # game splash/start screen
        self.start()

    def start(self):
        # game splash/start screen
        with self.start_screen:
            while self.game.waiting and self.game.running:
                self.start_screen.run()

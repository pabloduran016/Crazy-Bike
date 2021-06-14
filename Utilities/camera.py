from pymunk import Vec2d as Vec
from settings import SHAKE, SCROLL_DIVIDER
from random import randint
from Utilities import scale
from typing import Union, Tuple


class Camera:
    focus: Vec
    position: Vec = (0, 0)
    shake: int = 0

    def __init__(self, game, focus: Union[Tuple[float, float], Vec] = (0, 0)):
        self.game = game
        self.focus = Vec(*focus)

    def update(self) -> None:
        if not self.game.crushed:
            self.move()
        elif self.game.go_counter < 100:
            # print('death_Cam')
            self.death_cam()
        else:
            self.game.playing = False
        self.position = Vec(*self.game.scroll)
        self.apply_camera_shake()

    def apply_camera_shake(self) -> None:
        if self.shake:
            self.shake -= 1
            self.position += Vec(randint(-SHAKE, SHAKE), randint(-SHAKE, SHAKE))

    def death_cam(self) -> None:
        # TODO: fix bugs on the death cam, it doesn't put the bike on the centre
        # TODO: fix bugs on zooming, textures don't zoom properly
        self.game.zoom += 0.003
        self.game.scroll += (scale(self.game.board.image, self.game.board.dimensions,
                                   self.game.zoom).get_rect().center +
                   self.game.board.body.position * self.game.zoom - self.game.scroll - self.focus * self.game.zoom)
        self.game.go_counter += 1

    def move(self) -> None:
        scroll = scale(self.game.board.image, self.game.board.dimensions, self.game.zoom).get_rect().center + \
                 self.game.board.body.position * self.game.zoom - self.game.scroll - self.focus * self.game.zoom
        self.game.scroll += (scroll.x / SCROLL_DIVIDER[0], scroll.y / SCROLL_DIVIDER[1])
        self.game.distance = abs(self.game.backwheel.body.position.x / 5000)
        # TODO: add smooth zooming when going at high speeds

    def reset(self) -> None:
        self.position = Vec(0, 0)

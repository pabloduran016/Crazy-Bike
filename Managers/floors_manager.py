import pygame.draw
from pymunk import Vec2d as Vec
from Floors import *
from settings.FLOORS import *
from random import randint
from typing import List, Union, Tuple
# from game import Physics


class FloorsManager(pygame.sprite.Sprite):
    def __init__(self, game, physics):
        """
        :type game: game.Game
        """
        pygame.sprite.Sprite.__init__(self)
        self.all: List[Floor] = []
        self.game = game
        self.physics = physics

    def reset(self) -> None:
        self.all = []

    def start(self) -> None:
        self.all.append(HorizontalLine(game=self.game, physics=self.physics, position=Vec(*INITIALPOS), length=800,
                                       width=WIDTH))
        self.create_horizontalline(Vec(*INITIALPOS), 800)

    def update(self) -> None:
        lastfloor: Floor = self.all[-1]
        distance = (lastfloor.body.position*self.game.zoom - self.game.camera.position).length
        while distance < 3000*self.game.zoom:
            selection = randint(1, 2)
            le = randint(500, 1400)
            # selection = 2
            if selection == 1:
                self.create_line(lastfloor.lastpoint, le)
            elif selection == 2:  # PARABOLA
                self.create_parabola(lastfloor.lastpoint, le)
            lastfloor: Floor = self.all[-1]
            self.game.coin_manager.generate(self.all[-1])
            self.create_horizontalline(lastfloor.lastpoint, 500)
            self.game.coin_manager.generate(self.all[-1])
            lastfloor: Floor = self.all[-1]
            distance = (lastfloor.body.position - self.game.backwheel.body.position).length

        while len(self.all) > 30:
            self.all.pop(0)

    def create_horizontalline(self, position: Union[Vec, Tuple[float, float]], length: int) -> None:
        self.all.append(
            HorizontalLine(game=self.game, physics=self.physics, position=position, length=length,
                           width=WIDTH))

    def create_parabola(self, position: Union[Vec, Tuple[float, float]], length: int) -> None:
        if len(self.all) > 2:
            h = randint(-400, 800)
            if h + self.all[-2].lastpoint.y > INITIALPOS[1]:  # If you go down, do you reach de bottom?
                h = randint(-400, 0)
                self.all.append(Parabola(game=self.game, physics=self.physics, position=position,
                                         length=length, height=h, width=WIDTH, up=True))
            else:
                if h >= 0:
                    self.all.append(Parabola(game=self.game, physics=self.physics, position=position,
                                             length=length, height=h, width=WIDTH, up=False))
                else:
                    self.all.append(Parabola(game=self.game, physics=self.physics, position=position,
                                             length=length, height=h, width=WIDTH, up=True))
        else:
            # print('h')
            h = randint(-400, 0)
            self.all.append(Parabola(game=self.game, physics=self.physics, position=position,
                                     length=length, height=h, width=WIDTH, up=True))

    def create_line(self, position: Union[Vec, Tuple[float, float]], length: int) -> None:
        if len(self.all) > 2:  # LINE
            h = randint(-60 * length, 80 * length) / 100
            if h + self.all[-2].lastpoint.y > INITIALPOS[1]:  # If you go down, do you reach de bottom?
                h = randint(-60 * length, 0) / 100
        else:
            h = randint(-60 * length, 0) / 100
        self.all.append(Line(game=self.game, physics=self.physics, position=position,
                             final_pos=position + Vec(length, h), width=WIDTH))

    def draw(self) -> None:
        for floor in self.all:
            floor.draw()

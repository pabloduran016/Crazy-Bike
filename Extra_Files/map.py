import pygame.draw
from Extra_Files.createmap_copy import MapCreator
from settings import MAP
vec = pygame.Vector2


class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        :type game: main.Game
        """
        super().__init__()
        self.creator = MapCreator(MAP.INITIAL_Y)
        self.particles = []
        self.color = MAP.COLOR
        self.width = MAP.WIDTH
        self.totalx = self.creator.updatemap()
        self.game = game

    def update(self):
        if self.game.backwheel.body.position.x > self.totalx:
            self.totalx += self.creator.updatemap()

    def draw(self):
        for index, particle in enumerate(self.particles):
            if index != 0:
                pygame.draw.line(self.game.screen, self.color, self.particles[index - 1], particle, self.width)

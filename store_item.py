import pygame as pg
from settings.colors import *
from coin import SimpleCoin
from button import Button
import pygame.gfxdraw


class StoreItem:
    def __init__(self, font, text, size, price, dimensions, image, texture, obj, color=WHITE, **kwargs):
        self.rect = pg.Rect(0, 0, *dimensions)
        self.color = color
        self.activated = True
        self.image = pg.image.load(image).convert_alpha()
        self.image_rect = self.image.get_rect()
        self.item = text.split(' ')[0].lower()
        self.font = font
        self.price = price
        self.obj = obj
        self.text = [
            [self.font.get_rect(text=text, size=size), text, color, size, True, None],
            [self.font.get_rect(text=str(price), size=size), str(price), color, size, True, None],
        ]
        if 'image_width' in kwargs.keys():
            x = round(kwargs['image_width'])
            y = round(x * self.image_rect.height / self.image_rect.width)
        elif 'image_height' in kwargs.keys():
            y = round(kwargs['image_height'])
            x = round(y * self.image_rect.width / self.image_rect.height)
        else:
            x = round(dimensions[0] * .9)
            y = round(x * self.image_rect.height / self.image_rect.width)
        self.image = pg.transform.scale(self.image, (x, y))
        self.image_rect = self.image.get_rect()
        self.texture = texture
        if 'topright' in kwargs.keys():
            self.rect.topright = kwargs['topright']
        elif 'topleft' in kwargs.keys():
            self.rect.topleft = kwargs['topleft']
        elif 'bottomright' in kwargs.keys():
            self.rect.bottomright = kwargs['bottomright']
        elif 'bottomleft' in kwargs.keys():
            self.rect.bottomleft = kwargs['bottomleft']
        elif 'center' in kwargs.keys():
            self.rect.center = kwargs['center']
        self.image_rect.center = self.rect.center[0], self.rect.center[1]
        self.text[0][0].centerx, self.text[0][0].bottom = self.rect.centerx, self.rect.top + 40
        self.text[1][0].centerx, self.text[1][0].bottom = self.rect.centerx, self.rect.bottom - 20
        self.simple_coin = SimpleCoin(game=None, position=(0, 0))
        self.simple_coin.rect.left, self.simple_coin.rect.centery = self.text[1][0].right + 20, self.text[1][0].centery
        self.button = Button(size=dimensions, center=self.rect.center)

    def update(self):
        self.simple_coin.update()

    def draw(self, screen):
        pg.draw.rect(screen, self.color if self.activated else GREY, self.rect, width=10)
        pygame.gfxdraw.textured_polygon(screen, (self.rect.topleft, self.rect.topright, self.rect.bottomright,
                                                 self.rect.bottomleft), self.texture, 0, 0)
        for rect, text, color, size, activated, value in self.text:
            if activated:
                screen.blit(self.font.render(
                    text=text,
                    fgcolor=color,
                    size=size)[0], rect)
        self.simple_coin.draw(screen)
        screen.blit(self.image, self.image_rect)

    def purchase(self):
        self.activated = False

import pygame.sprite


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, *args):
        for obj in self.sprites():
            if hasattr(obj, 'draw'):
                obj.draw()

    def start(self):
        for obj in self.sprites():
            if hasattr(obj, 'start'):
                obj.start()

    def reset(self):
        for obj in self.sprites():
            if hasattr(obj, 'reset'):
                obj.reset()
        self.start()

    def apply_zoom(self, zoom):
        for obj in self.sprites():
            if hasattr(obj, 'apply_zoom'):
                obj.apply_zoom(zoom)

    def mouseclick(self, mouse):
        for obj in self.sprites():
            if hasattr(obj, 'mouseclick'):
                captured = obj.mouseclick(mouse)
                if captured:
                    return captured

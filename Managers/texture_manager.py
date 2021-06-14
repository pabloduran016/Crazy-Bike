from typing import Dict, Union, Tuple
import pygame as pg


class TextureManager:
    textures: Dict[str, Union[pg.Surface, pg.SurfaceType]] = {}

    def add(self, *args: Tuple[str, str]) -> None:
        for name, tex in args:
            if name not in self.textures.keys():
                self.textures[name] = pg.image.load(tex).convert()
                self.textures[name].set_colorkey((255, 255, 255))
            else:
                raise ValueError(f'Texutre with name {name} is already defined')

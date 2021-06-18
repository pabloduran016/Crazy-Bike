from pygame.sprite import Sprite
from abc import ABC, abstractmethod


class Screen(ABC, Sprite):
    @abstractmethod
    def __enter__(self) -> None:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

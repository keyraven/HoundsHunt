import pygame
from scripts.fonts import Fonts

class Room:

    def __init__(self):
        self.background = None
        self._all_sprites = pygame.sprite.Group()    
        pass

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        return self._all_sprites

class View:
    
    def __init__(self, background:pygame.Surface, ):


        pass

class Object:

    def __init__(self):
        pass
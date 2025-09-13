import pygame
from scripts.fonts import Fonts

class Room:

    def __init__(self):
        self.background = None
        self.all_sprites = pygame.sprite.Group()
        self.all_interactables = pygame.sprite.Group()
        pass
    
    def handle_event(self, event:pygame.Event):
        pass

class View:
    
    def __init__(self, background:pygame.Surface, ):


        pass

class Object:

    def __init__(self):
        pass
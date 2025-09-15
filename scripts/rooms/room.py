import pygame
from scripts.fonts import Fonts

class Room:

    def __init__(self):
        self.background = None
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_interactables = pygame.sprite.LayeredUpdates()
        pass
    
    def handle_event(self, event:pygame.Event):
        pass

class View:
    
    def __init__(self, background:pygame.Surface, ):


        pass

class Object:

    def __init__(self):
        pass
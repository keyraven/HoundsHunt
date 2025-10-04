import pygame
from scripts.fonts import Fonts

class Room:

    def __init__(self):
        self.background = None
        self.all_sprites = pygame.sprite.LayeredUpdates()
        pass
    
    def setup(self):
        return
    
        
    def teardown(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def handle_event(self, event:pygame.Event, active_item = None):
        pass

    def handle_ui_signals(self, event:pygame.Event, active_item = None):
        pass

    def draw(self, draw_surface: pygame.Surface):
        self.all_sprites.draw(draw_surface)

class View:
    
    def __init__(self, background:pygame.Surface, ):


        pass

class Object:

    def __init__(self):
        pass
from scripts.rooms.room import Room
from scripts.button import Button
from scripts.layeredsprite import LayeredSprite
import pygame

class InfoRoom(Room):
    
    def __init__(self):
        super().__init__()
        
        self.back_button = None


    def draw(self, draw_surface:pygame.Surface):
        draw_surface.blit(self.background, (0,0))

    def setup(self):
        self.background = pygame.image.load("./resources/StartScreen.png")

        
        LayeredSprite(pygame.Rect())
        
        self.back_button = Button()
        
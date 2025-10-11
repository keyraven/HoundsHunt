from scripts.rooms.room import Room
import pygame

class InfoRoom(Room):
    
    def __init__(self):
        
        self.background = pygame.image.load("./resources/StartScreen.png")

        super().__init__()

    def draw(self, draw_surface:pygame.Surface):
        draw_surface.blit(self.background, (0,0))

    def setup(self):
        pass
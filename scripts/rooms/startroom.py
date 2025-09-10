import scripts.rooms.room as room
import pygame
from scripts.fonts import Fonts


class StartRoom(room.Room):

    def __init__(self):
        super().__init__()
        
        self.heading_text = "Hound's Hunt"
        self.background = pygame.image.load("./resources/StartScreen.png")

    def setup(self):
        return

    def draw(self, draw_surface: pygame.Surface):
        # Runs every frame
        draw_surface.blit(self.background, (0,0))
        heading_text_sur = Fonts.preview_large.render(self.heading_text, False, "black")
        draw_surface.blit(heading_text_sur, (200, 250))

        self.all_sprites

        
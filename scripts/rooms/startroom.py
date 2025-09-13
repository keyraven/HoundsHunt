import scripts.rooms.room as room
import pygame
from scripts.fonts import Fonts
from scripts.button import Button


class StartRoom(room.Room):

    def __init__(self):
        super().__init__()
        
        self.heading_text = "Hound's Hunt"
        self.background = pygame.image.load("./resources/StartScreen.png")

    def setup(self):
        self.start_button = Button(pygame.Rect(340, 270, 100, 40), self.all_interactables, self.all_sprites,
                                   text="START", text_renderer=Fonts.preview_20, antialias=False,  background=pygame.Color("orange"))

    def teardown(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def draw(self, draw_surface: pygame.Surface):
        # Runs every frame
        draw_surface.blit(self.background, (0,0))
        heading_text_sur = Fonts.preview_50.render(self.heading_text, False, "black")
        draw_surface.blit(heading_text_sur, (200, 220))

        self.all_sprites.draw(draw_surface)

        
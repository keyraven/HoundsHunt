import scripts.rooms.room as room
import pygame
from scripts.fonts import Fonts
from scripts.button import Button
from scripts.custiom_events import CustomEvent


class StartRoom(room.Room):

    def __init__(self):
        super().__init__()
        
        self.heading_text = "Hound's Hunt"
        self.background = None

    def setup(self):
        
        self.background = pygame.image.load("./resources/StartScreen.png")
        start_theme = {
            "background": "orange",
            "hover_background": "orange2",
            "active_background": "orangered",
            "text_color": "black"
        }

        self.start_button = Button(pygame.Rect(340, 270, 100, 40), self.all_sprites,
                                   text="START", text_renderer=Fonts.preview_20, antialias=False, theme=start_theme)
    def teardown(self):
        super().teardown()
        self.background = None

    def draw(self, draw_surface: pygame.Surface):
        # Runs every frame
        draw_surface.blit(self.background, (0,0))
        heading_text_sur = Fonts.preview_50.render(self.heading_text, False, "black")
        draw_surface.blit(heading_text_sur, (200, 220))

        self.all_sprites.draw(draw_surface)

    def handle_event(self, event):
        
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite == self.start_button:
                pygame.event.post(pygame.Event(CustomEvent.CHANGE_ROOM, {"room":"room1"}))

        
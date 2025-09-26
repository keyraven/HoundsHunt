from scripts.rooms.room import Room
import pygame
from scripts.custiom_events import CustomEvent
from scripts.animatedinteractable import AnimatedInteractable

class Room1(Room):

    def __init__(self):
        super().__init__()

        self.background = pygame.image.load("./resources/room1.png")

    def setup(self):
        #Send Signal to Open UI
        pygame.event.post(pygame.event.Event(CustomEvent.TO_UI, {"action": "open"}))

        (glitter_frames, glitter_mask) = AnimatedInteractable.get_frames_dir("resources/glitter_animation")

        self.glitter = AnimatedInteractable(pygame.Rect(175, 32, glitter_frames[0].get_width(), glitter_frames[0].get_height()), 
                                             glitter_frames, self.all_sprites, speed = 10, hover_speed = 6, 
                                             mask=glitter_mask)

    def draw(self, draw_surface):
        draw_surface.blit(self.background, (0,0))
        super().draw(draw_surface)
        

from scripts.interactable import Interactable
from scripts.custiom_events import CustomEvent
import pygame
import pygame.freetype

class Button(Interactable):

    def __init__(self, rect:pygame.Rect, *groups, background: pygame.Color, text:str, text_renderer:pygame.freetype.Font, text_size:int, text_color:pygame.Color = None, image:pygame.Surface = None, hotkey = None, when_interacted = None):
        super().__init__(rect, *groups, image=image, hotkey=hotkey, when_interacted=when_interacted, background=background)

        self.text = text
        self.text_renderer = text_renderer

        self.text_color = text_color if text_color is not None else pygame.Color("black")
        self.text_size = text_size
        text, rect = self.text_renderer.render(text, self.text_color, size=self.text_size)
        
        pygame.Surface.blit(self.image, text, (self.rect.width/2 - text.width/2, self.rect.height/2 - text.height/2))

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def process_event(self, event:pygame.Event) -> bool:
        
        hit = False
        #Check Hotkey
        if event.type == pygame.KEYUP:
            if event.key == self.hotkey:
                pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_HOTKEY, {"sprite": self}))
                hit = True

        #Check MouseClick
        if not self.hover: # If not hovering over the button, don't bother with checking for mouseclick
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_KEYDOWN, {"sprite": self}))
            hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_KEYUP, {"sprite": self}))
            hit = True

        return hit


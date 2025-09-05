from scripts.interactable import Interactable
from scripts.custiom_events import CustomEvent
import pygame

class Button(Interactable):

    def __init__(self, rect:pygame.Rect, *groups, text:str, text_renderer:pygame.Font, image:pygame.Surface = None, hotkey = None, when_interacted = None):
        super().__init__(rect, *groups, image=image, hotkey=hotkey, when_interacted=when_interacted)

        self.text = text
        self.text_renderer = text_renderer
        self.hover = False


    def check_hover_state(self, mouse_location:tuple):
        
        if self.rect.contains(mouse_location):
            self.hover = True
        else:
            self.hover = False

    def get_event_queue_object(self, trigger_event_type:int) -> pygame.Event:

        

        if not self.hover: # If not hovering over the button, don't bother with checking for mouseclick
            pass
        elif trigger_event_type == pygame.MOUSEBUTTONDOWN:
            event_type = CustomEvent.BUTTON_KEYDOWN
        elif trigger_event_type == pygame.MOUSEBUTTONUP:
            return

import pygame
from scripts.custiom_events import CustomEvent

class Interactable(pygame.sprite.Sprite):

    all_interactables:pygame.sprite.Group = None

    def __init__(self, rect:pygame.Rect, *groups, image:pygame.Surface = None, hotkey:str = None, when_interacted:callable = None):
        super().__init__(*groups)

        self.hotkey = hotkey
        self.when_interacted = when_interacted
        self.rect = rect
        if self.image is not None: 
            self.rect.height = self.image.get_height()
            self.rect.width = self.image.get_width()

        if Interactable.all_interactables is None:
            Interactable.all_interactables = pygame.sprite.Group()
        
        Interactable.all_interactables.add(self)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def get_event_queue_object(self, trigger_event_type:pygame.Event) -> pygame.Event:
        return pygame.Event(CustomEvent.INTERACT, parent_object = self)

    def interact(self):
        if self.when_interacted is not None: 
            self.when_interacted()


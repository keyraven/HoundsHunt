import pygame
from scripts.custiom_events import CustomEvent

class Interactable(pygame.sprite.Sprite):

    def __init__(self, rect:pygame.Rect, *groups, image:pygame.Surface = None, background:pygame.color.Color, hotkey:str = None, when_interacted:callable = None):
        super().__init__(*groups)

        self.hotkey = hotkey
        self.when_interacted = when_interacted
        self.rect = rect
        if image is not None: 
            self.rect.height = self.image.get_height()
            self.rect.width = self.image.get_width()
        self.hover=False
        
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(background)
        
        if image is not None:
            pygame.Surface.blit(self.image, image, (0,0))


    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def check_hover_state(self, mouse_location:tuple) -> bool:
        if self.rect.collidepoint(mouse_location):
            self.hover = True
        else:
            self.hover = False

        return self.hover

    def interact(self):
        if self.when_interacted is not None: 
            self.when_interacted()



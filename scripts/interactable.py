import pygame
from scripts.custiom_events import CustomEvent

"""
Theme Parameters:

"background" = #rrggbbaa OR "colorname"
"hover_background" = #rrggbbaa OR "colorname"
"active_background" = #rrggbbaa OR "colorname"
"disabled_background" = #rrggbbaa OR "colorname"
"text_color" = #rrggbbaa OR "colorname"
"hover_text_color" = #rrggbbaa OR "colorname"
"active_text_color" = #rrggbbaa OR "colorname"
"disabled_text_color" = #rrggbbaa OR "colorname"
"image" = pygame.surface
"hover_image" = pygame.surface
"active_image" = pygame.surface
"disabled_image" = pygame.surface
"scale_image" = False

"""


class Interactable(pygame.sprite.Sprite):

    theme_defaults = {
        "background": "#00000000",
    }


    def __init__(self, rect:pygame.Rect, *groups, hotkey:int = None, theme:dict = None):
        super().__init__(*groups)

        self.hotkey = hotkey
        self.rect = rect
        self.active =  False
        self.hover = False
        self.disabled = False

        self.theme = theme if theme is not None else {}
        self.background = self.theme.get("background", self.theme_defaults["background"])
        self.hover_background = self.theme.get("hover_background", self.background)
        self.active_background = self.theme.get("active_background", self.hover_background)
        self.disabled_background = self.theme.get("disabled_background", self.background)

        self.normal_image = self.theme.get("image")
        self.hover_image = self.theme.get("hover_image", self.normal_image)
        self.active_image = self.theme.get("active_image", self.hover_image)
        self.disabled_image = self.theme.get("disabled_image", self.normal_image)
        if self.theme.get("scale_image", False):
            self.normal_image = self._scale_image(self.normal_image)
            self.hover_image = self._scale_image(self.hover_image)
            self.active_image = self._scale_image(self.active_image)
            self.disabled_image = self._scale_image(self.disabled_image)

        self.normal_surface = None
        self.hover_surface = None
        self.active_surface = None
        self.disabled_surface = None
    
    def build_surfaces(self) -> pygame.Surface:

        self.normal_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.normal_surface.fill(self.background)
        if self.normal_image is not None:
            self.normal_surface.blit(self.normal_image, (self.rect.width.get_width()/2 - self.normal_image.get_width()/2,
                                                         self.rect.height.get_height()/2 - self.normal_image.get_height()/2))
            
        if self.hover_background == self.background and self.hover_image == self.normal_image:
            self.hover_surface = self.normal_surface
        else:
            self.hover_surface = pygame.Surface((self.rect.width, self.rect.height))
            self.hover_surface.fill(self.hover_background)
            if self.hover_image is not None:
                self.hover_surface.blit(self.hover_image, (self.rect.width.get_width()/2 - self.hover_image.get_width()/2,
                                                         self.rect.height.get_height()/2 - self.hover_image.get_height()/2))
                
        if self.active_background == self.hover_background and self.active_image == self.normal_image:
            self.active_surface = self.hover_surface
        else:
            self.active_surface = pygame.Surface((self.rect.width, self.rect.height))
            self.active_surface.fill(self.active_background)
            if self.active_image is not None:
                self.active_surface.blit(self.active_image, (self.rect.width.get_width()/2 - self.active_image.get_width()/2,
                                                         self.rect.height.get_height()/2 - self.active_image.get_height()/2))
                
        if self.disabled_background == self.background and self.disabled_image == self.normal_image:
            self.disabled_surface = self.normal_surface
        else:
            self.disabled_surface = pygame.Surface((self.rect.width, self.rect.height))
            self.disabled_surface.fill(self.disabled_background)
            if self.disabled_image is not None:
                self.active_surface.blit(self.disabled_image, (self.rect.width/2 - self.disabled_image.get_width()/2,
                                                         self.rect.height/2 - self.disabled_image.get_height()/2))

    def _scale_image(self, surface:pygame.Surface) -> pygame.Surface:
        if type(surface) == pygame.Surface:
            if surface.get_width() > self.rect.width or surface.get_height() > self.rect.height:
                if surface.get_width() > surface.get_height():
                    scale = self.rect.width/surface.get_width()
                else:
                    scale = self.rect.height/surface.get_height()
                surface = pygame.transform.scale_by(surface, scale)

        return surface
        

    def update(self, *args, **kwargs):
        if self.normal_image == None:
            self.build_surfaces()

        if self.disabled:
            self.image = self.disabled_surface
        elif self.active:
            self.image = self.active_surface
        elif self.hover:
            self.image = self.hover_surface
        else:
            self.image = self.normal_surface

        return super().update(*args, **kwargs)
    
    def check_hover_state(self, mouse_location:tuple) -> bool:
        if self.rect.collidepoint(mouse_location):
            self.hover = True
        else:
            self.hover = False
            self.active = False
        return self.hover

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
            self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_KEYUP, {"sprite": self}))
            hit = True
            self.active = False

        return hit


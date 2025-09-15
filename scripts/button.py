from scripts.interactable import Interactable
from scripts.custiom_events import CustomEvent
import pygame

class Button(Interactable):

    theme_defaults = {
        "background": "#00000000",
        "text_color":  "#000000FF",
        "hover_text_color": "#313131FF",
        "active_text_color": "#313131FF",
        "disabled_text_color": "#7B7B7BFF",
        "shape": "rect",
        "scale_image": False
    }

    def __init__(self, rect:pygame.Rect, *groups, text:str, text_renderer:pygame.Font, antialias:bool = True, theme:dict = None, hotkey = None):
        super().__init__(rect, *groups, hotkey=hotkey, theme=theme)

        self.text = text
        self.text_renderer = text_renderer
        self.antialias = antialias
        self.text_color = theme.get("text_color", theme["text_color"])
        self.hover_text_color = theme.get("hover_text_color", self.text_color)
        self.active_text_color = theme.get("hover_text_color", self.hover_text_color)
        self.disabled_text_color = theme.get("disabled_text_color", self.text_color)

    
    def build_surfaces(self):
        super().build_surfaces()

        normal_text = self.text_renderer.render(self.text, self.antialias, self.text_color)
        normal_text = self._scale_image(normal_text)
        self.normal_surface.blit(normal_text, (self.rect.width/2 - normal_text.get_width()/2, 
                                               self.rect.height/2 - normal_text.get_height()/2))
        
        if self.hover_surface != self.normal_surface:
            hover_text = self.text_renderer.render(self.text, self.antialias, self.hover_text_color)
            self.hover_surface.blit(hover_text, (self.rect.width/2 - hover_text.get_width()/2, 
                                                 self.rect.height/2 - hover_text.get_height()/2))
            
        if self.active_surface != self.hover_surface:
            active_text = self.text_renderer.render(self.text, self.antialias, self.active_text_color)
            self.active_surface.blit(active_text, (self.rect.width/2 - active_text.get_width()/2, 
                                                   self.rect.height/2 - active_text.get_height()/2))
            
        if self.disabled_surface != self.normal_surface:
            disabled_text = self.text_renderer.render(self.text, self.antialias, self.disabled_text_color)
            self.disabled_surface.blit(disabled_text, (self.rect.width/2 - disabled_text.get_width()/2, 
                                                       self.rect.height/2 - disabled_text.get_height()/2))


import pygame
from scripts.custiom_events import CustomEvent
from scripts.layeredsprite import LayeredSprite

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
"shape: = "rect" or "poly((9,2)(6,8)(6,8))", "round"


"""


class Interactable(LayeredSprite):

    theme_defaults = {
        "background": "#00000000",
        "shape": "rect",
        "scale_image": False
    }

    def __init__(self, rect:pygame.Rect, groups = (), hotkey:int = None, theme:dict = None, layer:int = 0, 
                 collide_on_vis:bool = False, mask:pygame.Mask = None, id = None, visible:bool = True):
        super().__init__(rect, groups=groups, layer=layer, theme=theme, collide_on_vis=collide_on_vis, mask=mask,
                         id=id, visible=visible)

        self.hotkey = hotkey
        self.active =  False
        self.hover = False
        self.disabled = False
       
        self.hover_background = self.theme.get("hover_background", self.background)
        self.active_background = self.theme.get("active_background", self.hover_background)
        self.disabled_background = self.theme.get("disabled_background", self.background)

        self.hover_image = self.theme.get("hover_image", self.normal_image)
        self.active_image = self.theme.get("active_image", self.hover_image)
        self.disabled_image = self.theme.get("disabled_image", self.normal_image)

    
        if self.theme.get("scale_image", self.theme_defaults["scale_image"]):
            self.hover_image = self._scale_image(self.hover_image)
            self.active_image = self._scale_image(self.active_image)
            self.disabled_image = self._scale_image(self.disabled_image)

        self.hover_surface:LayeredSprite.SurfaceWithMask = None
        self.active_surface:LayeredSprite.SurfaceWithMask = None
        self.disabled_surface:LayeredSprite.SurfaceWithMask = None

    def build_surfaces(self) -> pygame.Surface:
        super().build_surfaces()

        if self.hover_background == self.background and self.hover_image == self.normal_image:
            self.hover_surface = self.normal_surface
        else:
            hover_surface = pygame.Surface((self.rect.width, self.rect.height),pygame.SRCALPHA)
            self._draw_background_shape(hover_surface, self.hover_background)
            if self.hover_image is not None:
                hover_surface.blit(self.hover_image, (self.rect.width.get_width()/2 - self.hover_image.get_width()/2,
                                                      self.rect.height.get_height()/2 - self.hover_image.get_height()/2))
            self.hover_surface = self.SurfaceWithMask(hover_surface, create_mask=self.collide_on_vis)
                
        if self.active_background == self.hover_background and self.active_image == self.hover_image:
            self.active_surface = self.hover_surface
        else:
            active_surface = pygame.Surface((self.rect.width, self.rect.height),pygame.SRCALPHA)
            self._draw_background_shape(active_surface, self.active_background)
            if self.active_image is not None:
                active_surface.blit(self.active_image, (self.rect.width.get_width()/2 - self.active_image.get_width()/2,
                                                         self.rect.height.get_height()/2 - self.active_image.get_height()/2))
            self.active_surface = self.SurfaceWithMask(active_surface, create_mask=self.collide_on_vis)
            
                
        if self.disabled_background == self.background and self.disabled_image == self.normal_image:
            self.disabled_surface = self.normal_surface
        else:
            disabled_surface = pygame.Surface((self.rect.width, self.rect.height))
            self._draw_background_shape(disabled_surface, self.disabled_background)
            if self.disabled_image is not None:
                disabled_surface.blit(self.disabled_image, (self.rect.width/2 - self.disabled_image.get_width()/2,
                                                            self.rect.height/2 - self.disabled_image.get_height()/2))
            self.disabled_surface = self.SurfaceWithMask(disabled_surface, create_mask=self.collide_on_vis)

    def change_layer(self, new_layer:int):
        self.layer = new_layer
        for g in self.groups():
            try:
                g.change_layer(self, new_layer)
            except AttributeError:
                pass
    
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        self._image = self.get_draw_surface()

        return 
    
    def get_draw_surface(self) -> LayeredSprite.SurfaceWithMask:

        if self.disabled:
            return self.disabled_surface
        elif self.active:
            return self.active_surface
        elif self.hover:
            return self.hover_surface
    
        
        return self.normal_surface

    def check_hover_state(self, mouse_location:tuple) -> bool:
        if self.collidepoint(mouse_location):
            self.hover = True
        else:
            self.hover = False
            self.active = False
        return self.hover
    
    def process_event(self, event:pygame.Event) -> bool:
        
        if self.disabled or not self.visible:
            return False

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


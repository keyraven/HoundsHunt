from scripts.custiom_events import CustomEvent
import pygame
import re

class LayeredSprite(pygame.sprite.Sprite):
    
    theme_defaults = {
        "background": "#00000000",
        "shape": "rect",
        "scale_image": True
    }

    empty_surface = pygame.Surface((0,0))

    class SurfaceWithMask():
        
        def __init__(self, surface:pygame.Surface, mask:pygame.Mask = None, create_mask:bool = False):
            
            self.surface = surface
            self._create_mask = create_mask
            self.id = id

            if self._create_mask:
                self.mask = pygame.mask.from_surface(self.surface)
            else:
                self.mask = mask

        @property
        def create_mask(self):
            return self._create_mask
        
        @create_mask.setter
        def create_mask(self, value:bool):
            
            if self._create_mask == value:
                return

            self._create_mask = value
            if value:
                self.mask = pygame.mask.from_surface(self.surface)

        def blit(self,
                source: pygame.Surface,
                dest = (0, 0),
                area = None,
                special_flags: int = 0,
                lock_mask:bool = False):
            
            self.surface.blit(source, dest, area, special_flags)
            
            if self.create_mask and not lock_mask:
                self.mask = pygame.mask.from_surface(self.surface)

        def mask_union(self, new_mask:pygame.mask.Mask):
            if self.mask is None:
                self.mask = new_mask
            else:
                self.mask = new_mask.draw(self.mask)

        def copy(self):
            mask_copy = None if self.mask is None else self.mask.copy()
            copy = LayeredSprite.SurfaceWithMask(self.surface.copy(), mask_copy)
            copy._create_mask = self._create_mask
            return copy

    def __init__(self, rect, groups = (), layer:int = 0, image:pygame.Surface = None, theme:dict = None, 
                 collide_on_vis:bool = False, mask:pygame.Mask = None, id = None, visible:bool = True):
        super().__init__()

        self.layer = layer
        if type(groups) is not tuple or type(groups) is not list:
            groups = [groups]
        for g in groups:
            g.add(self)

        self.rect = rect
        self._mask = mask
        self.collide_on_vis = collide_on_vis 
        self.id = id
        self.visible = visible
        self.process_clicks = False

        self.theme = theme if theme is not None else {}
        for x in self.theme:
            if type(self.theme[x]) is str:
                self.theme[x] = self.theme[x].strip()

        self.theme = {}
        self.update_theme(theme)

        self.normal_image = self.theme.get("image") if image is None else image
        if self.theme.get("scale_image", self.theme_defaults["scale_image"]):
            self._scale_image(self.normal_image)

        self.normal_surface:LayeredSprite.SurfaceWithMask = None

        self._image:LayeredSprite.SurfaceWithMask = None

    @property
    def image(self):
        if self.visible:
            return self._image.surface
        else:
            return self.empty_surface
    
    @property
    def mask(self):
        if not self.visible:
            return None
        
        if self._image.mask is None:
            return self.normal_surface.mask
        
        return self._image.mask
    
    def update_image(self, new_image:pygame.Surface):
        if new_image is None:
            self.normal_image = self.empty_surface
            self.normal_surface = None # Triggers rebuild on next update. 

        self.normal_image = new_image 
        if self.theme.get("scale_image", self.theme_defaults["scale_image"]):
            self.normal_image = self._scale_image(self.normal_image)

        self.normal_surface = None # Triggers rebuild on next update. 

    def update_theme(self, new_theme:dict, clear_old = False):
        if new_theme is None:
            new_theme = {}

        if clear_old:
            self.theme = new_theme
        else:
            self.theme.update(new_theme)

        self.background = self.theme.get("background", self.theme_defaults["background"])

        self.shape = self.theme.get("shape", self.theme_defaults["shape"])

        self.normal_surface = None # This trigger re-drawing of the surfaces. 

    def _scale_image(self, surface:pygame.Surface) -> pygame.Surface:
        if surface is None:
            return None
        
        if surface.get_width() > self.rect.width or surface.get_height() > self.rect.height:
            if surface.get_width() > surface.get_height():
                scale = self.rect.width/surface.get_width()
            else:
                scale = self.rect.height/surface.get_height()
            surface = pygame.transform.scale_by(surface, scale, )

        return surface

    def _draw_background_shape(self, surface_to_draw:pygame.Surface, color) -> pygame.Surface:
        if self.shape == "rect":
            surface_to_draw.fill(color)
        elif self.shape.startswith("poly"):
            points = []
            for match in re.findall(r"\(([0-9 ]+),([0-9 ]+)\)", self.shape):
                points.append([int(i.strip()) for i in match])
            pygame.draw.polygon(surface_to_draw, pygame.Color(color), points)
        elif self.shape == "round":
            pygame.draw.ellipse(surface_to_draw, pygame.Color(color), surface_to_draw.get_rect())

        return surface_to_draw
    
    def collidepoint(self, point:tuple) -> bool:
        if not self.visible:
            return False

        if self.rect.collidepoint(point):
            if self.mask is None:
                return True
            
            relx = point[0] - self.rect.x
            rely = point[1] - self.rect.y
            if self.mask.get_at((relx, rely)):
                return True

        return False

    def process_event(self, event:pygame.Event) -> bool:
        if not self.process_clicks or not self.visible:
            return False
        
        hit = False
        if event.type == pygame.MOUSEBUTTONDOWN and self.collide_on_vis(event.pos):
            pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_KEYDOWN, {"sprite": self}))
            hit = True
        elif event.type == pygame.MOUSEBUTTONUP and self.collide_on_vis(event.pos):
            pygame.event.post(pygame.event.Event(CustomEvent.BUTTON_KEYUP, {"sprite": self}))
            hit = True

        return hit

    def build_surfaces(self) -> pygame.Surface:

        normal_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self._draw_background_shape(normal_surface, self.background)
        if self.normal_image is not None:
            normal_surface.blit(self.normal_image, (self.rect.width/2 - self.normal_image.get_width()/2,
                                                    self.rect.height/2 - self.normal_image.get_height()/2))
        self.normal_surface = self.SurfaceWithMask(normal_surface, self._mask, create_mask=self.collide_on_vis)

        self._image = self.normal_surface
            
    def update(self, *args, **kwargs):
        if self.normal_surface == None:
            self.build_surfaces()




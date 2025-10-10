import pygame
from scripts.custiom_events import CustomEvent
from scripts.interactable import Interactable

class Room:

    def __init__(self):
        self.background = None
        self._all_sprites = pygame.sprite.LayeredUpdates()

        self.current_view:View = None
        pass
    
    @property
    def all_sprites(self):
        if self.current_view is None:
            return self._all_sprites
        else:
            return self.current_view.all_sprites
    
    def setup(self):
        return
           
    def teardown(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def handle_event(self, event:pygame.Event, active_item = None):
        pass

    def draw(self, draw_surface: pygame.Surface):
        self.all_sprites.draw(draw_surface)

class View:
    
    def __init__(self, background:pygame.Surface, id, 
                 build_function:callable = None):
        
        self.background = background
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.build_function = build_function
        self.built = False
        self.id = id
        
        # Connections
        self.right:View = None
        self.left:View = None
        self.down:View = None

        self.right_arrow = None
        self.left_arrow = None
        self.down_arrow = None

        self.left_arrow_rect = pygame.Rect(14, 28, 38, 202)
        self.left_arrow_theme = {
            "shape": "poly((38,0)(28, 101)(38,202)(0,101))",
            "background": "#6B573D",
            "hover_background": "#93803E",
            "disabled_background": "#1B1911",
        }
        self.right_arrow_rect = pygame.Rect(588, 28, 38, 202)
        self.right_arrow_theme = {
            "shape": "poly((0,0)(10, 101)(0,202)(38,101))",
            "background": "#6B573D",
            "hover_background": "#93803E",
            "disabled_background": "#1B1911",
        }
        self.down_arrow_rect = pygame.Rect()
        self.down_arrow_theme = {
            "background": ""
        }

        self.hide()

    def draw_background(self, draw_surface):
        draw_surface.blit(self.background, (0,0))

    def setup(self):
        self.built = True
        
        # Set Arrows
        if self.right: 
            self.right_arrow = Interactable(self.right_arrow_rect, self.all_sprites, 
                                            theme=self.right_arrow_theme, layer = 20, collide_on_vis=True)
        if self.left:
            self.left_arrow = Interactable(self.left_arrow_rect, self.all_sprites, 
                                           theme=self.left_arrow_theme, layer = 20, collide_on_vis=True)
        if self.down:
            self.down_arrow = Interactable(self.down_arrow_rect, self.all_sprites, 
                                           theme=self.down_arrow_theme, layer = 20, collide_on_vis=True)
            
        if self.build_function is not None:
            self.build_function(self.all_sprites)

    def show(self):
        if not self.built:
            self.setup()
        
        for x in self.all_sprites:
            x.visible = True
    
    def hide(self):
        for x in self.all_sprites:
            x.visible = False

    def kill(self):
        for x in self.all_sprites:
            x.kill()

    def handle_arrow_event(self, event:pygame.Event):
        """Handles an events in the view. If the view needs to be changed, returns a
         view object. """
        
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite == self.right_arrow:
                return self.right
            elif event.sprite == self.left_arrow:
                return self.left
            elif event.sprite == self.down_arrow:
                return self.down
        
        return None
    
    def handle_event(self, event:pygame.Event):
        return





import pygame
from scripts.custiom_events import CustomEvent
from scripts.interactable import Interactable

class Room:

    def __init__(self):
        self.background = None
        self._all_sprites = pygame.sprite.LayeredUpdates()

        self._current_view:View = None
        pass
    
    @property
    def all_sprites(self):
        if self.current_view is None:
            return self._all_sprites
        else:
            return self.current_view.all_sprites
        
    @property
    def current_view(self):
        return self._current_view
    
    @current_view.setter
    def current_view(self, value):
        self._current_view.hide()
        self._current_view = value
        self._current_view.show()
    
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
        self.up:View = None

        self.right_arrow = None
        self.left_arrow = None
        self.down_arrow = None
        self.up_arrow = None

        arrow_colors = {
            "background": "#6B573D",
            "outline":3,
            "outline_color": "#1D150C",
            "hover_outline_color": "#523C23",
            "hover_background": "#93803E",
            "disabled_background": "#1B1911",
            }

        self.left_arrow_rect = pygame.Rect(14, 28, 38, 202)
        self.left_arrow_theme = arrow_colors | {
            "shape": "poly((38,0)(28, 101)(38,202)(2,101))",
        }
        self.right_arrow_rect = pygame.Rect(588, 28, 38, 202)
        self.right_arrow_theme = arrow_colors | {
            "shape": "poly((0,0)(10, 101)(0,202)(36,101))",
        }
        self.down_arrow_rect = pygame.Rect(219, 308, 202, 38)
        self.down_arrow_theme = arrow_colors | {
            "shape": "poly((0,0)(101, 10)(202,0)(101,36))",
        }
        self.up_arrow_rect = pygame.Rect(219, 14, 202, 38)
        self.up_arrow_theme = arrow_colors | {
            "shape": "poly((0,38)(101, 28)(202,38)(101,2))",
        }

        self.arrow_layer = 20

        self.hide()

    def update_arrow_theme(self, value:dict):

        self.up_arrow_theme.update(value)
        self.down_arrow_theme.update(value)
        self.right_arrow_theme.update(value)
        self.left_arrow_theme.update(value)

        self.trigger_rebuild()

    def draw_background(self, draw_surface):
        draw_surface.blit(self.background, (0,0))

    def setup(self):
        self.built = True
        
        # Set Arrows
        if self.right: 
            self.right_arrow = Interactable(self.right_arrow_rect, self.all_sprites, 
                                            theme=self.right_arrow_theme, layer = self.arrow_layer, collide_on_vis=True)
        if self.left:
            self.left_arrow = Interactable(self.left_arrow_rect, self.all_sprites, 
                                           theme=self.left_arrow_theme, layer = self.arrow_layer, collide_on_vis=True)
        if self.down:
            self.down_arrow = Interactable(self.down_arrow_rect, self.all_sprites, 
                                           theme=self.down_arrow_theme, layer = self.arrow_layer, collide_on_vis=True)
        if self.up:
            self.up_arrow = Interactable(self.up_arrow_rect, self.all_sprites, 
                                           theme=self.up_arrow_theme, layer = self.arrow_layer, collide_on_vis=True)
            
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

    def trigger_rebuild(self):
        """Triggers rebuild on next show"""
        self.built = False
        self.kill()

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
            elif event.sprite == self.up_arrow:
                return self.up
        
        return None
    
    def handle_event(self, event:pygame.Event):
        return





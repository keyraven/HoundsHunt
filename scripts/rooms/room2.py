from scripts.rooms.room import Room, View
import pygame
from scripts.custiom_events import CustomEvent
from scripts.animatedinteractable import AnimatedInteractable
from scripts.interactable import Interactable


class Room2(Room):

    def __init__(self):
        super().__init__()
    

        view1_background = pygame.image.load("resources/room2/view1.png")
        view1 = View(view1_background, 1, build_function=Room2.build_view_1)
        view2_background = pygame.image.load("resources/room2/view2.png")
        view2 = View(view2_background, 2, build_function=Room2.build_view_2)
        view3_background = pygame.image.load("resources/room2/view3.png")
        view3 = View(view3_background, 3, build_function=Room2.build_view_3)
        view4_background = pygame.image.load("resources/room2/view4.png")
        view4 = View(view4_background, 4, build_function=Room2.build_view_4)

        # Connections
        view1.right = view2      
        view1.left = view3
        view2.right = view3
        view2.left = view1
        view3.right = view4
        view3.left = view2
        view4.right = view1
        view4.left = view3

        # Look-in Views:
        lookin_background = pygame.image.load("resources/room2/view2-close.png")
        self.lookinview2 = View(lookin_background, 5, build_function=Room2.build_lookinview_2)
        self.lookinview2.down = view2
        
        lookin_background = pygame.image.load("resources/room2/lookindown.png")
        self.lookindown = View(lookin_background, 6, build_function=Room2.build_lookinview_2)
        self.lookindown.up = view1

        view1.down = self.lookindown
        view2.down = self.lookindown
        view3.down = self.lookindown
        view4.down = self.lookindown

        self._current_view = view1
        self._current_view.show()
    

    def draw(self, draw_surface):
        draw_surface.blit(self.current_view.background, (0,0))
        super().draw(draw_surface)

    @Room.current_view.setter
    def current_view(self, value):
        if value != self.lookindown:
            self.lookindown.up = value
        super(Room2, type(self)).current_view.fset(self, value)

    def handle_event(self, event, active_item=None):
        
        # Handle Changing View
        change_view = None
        if self.current_view is not None:
            change_view = self.current_view.handle_arrow_event(event)

        if change_view is not None:
            self.current_view = change_view

        if self.current_view.id == 1:
            self.handle_view_1_events(event, active_item)
        elif self.current_view.id == 2:
            self.handle_view_2_events(event, active_item)
        elif self.current_view.id == 3:
            self.handle_view_3_events(event, active_item)
        elif self.current_view.id == 4:
            self.handle_lookinview_2_events(event, active_item)

        
    def handle_view_1_events(self, event, active_item=None):
        return

    def handle_view_2_events(self, event, active_item=None):
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "tree_lookin":
                self.current_view = self.lookinview2
    
    def handle_view_3_events(self, event, active_item=None):
        return
    
    def handle_lookinview_2_events(self, event, active_item=None):
        return

    def handle_lookindown_events(all_sprites):
        return

    def build_view_1(all_sprites):
        return
    
    def build_view_2(all_sprites):
        
        # Interactable to enter into the close-view tree look
        theme = {
            #"background": "black"
        }
        Interactable(pygame.Rect(312, 63, 108, 157), all_sprites, theme=theme, id="tree_lookin")
        
    
    def build_view_3(all_sprites):
        return
    
    def build_view_4(all_sprites):
        return
    
    def build_lookinview_2(all_sprites):
        return
    
    def build_lookindown(all_sprites):
        return
        
    

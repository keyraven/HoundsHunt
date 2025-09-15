import scripts.rooms.room as r
from scripts.rooms.startroom import StartRoom
from scripts.rooms.room1 import Room1
from scripts.fonts import Fonts
import pygame
from scripts.interactable import Interactable
from scripts.button import Button
from scripts.custiom_events import CustomEvent
import random

"""
Holds all info regarding the game-state. 
"""
class Game:
    
    def __init__(self):
        #Start Class Variables

        self.i = 0
        self.rooms = {
            "start_room": StartRoom,
            "room1": Room1
        }
        self.inventory = []
        self.current_room:r = None
        self.change_room("start_room")
        
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.ui_open = False
        
        return

    """Loads game from file"""
    def load_game(self) -> None:
        raise NotImplementedError

    @property 
    def all_sprites(self) -> pygame.sprite.Group:
        return self.current_room.all_sprites
    
    @property
    def all_interactables(self) -> pygame.sprite.Group:
        return self.current_room.all_interactables
    
    def draw(self, pixel_screen: pygame.Surface):
        self.current_room.draw(pixel_screen)

    def update_all_sprites(self) -> pygame.sprite.Group:
        all_sprites = self.get_all_sprites()
        all_sprites.update()
        return self.get_all_sprites()
    
    def visual_tests(self, draw_screen:pygame.Surface):
        if self.i % 2:
            draw_screen.fill("purple")
        else:
            draw_screen.fill("orange")
        return
    
    def change_room(self, new_room_key:str):
        if self.current_room is not None:
            self.current_room.teardown()
        self.current_room = self.rooms[new_room_key]()
        self.current_room.setup()

    def update(self):
        self.all_sprites.update()

    def handle_mouselocation(self, mouseLocation:tuple):
        for interactable in self.all_interactables:
            hit = interactable.check_hover_state(mouseLocation)
            if hit:
                break

    def setup_ui(self):
        if self.ui_open:
            return
        
        self.ui_open = True

    def teardown_ui(self):
        if not self.ui_open:
            return
        
        self.ui_open = False

    def _handle_ui_event(self, event:pygame.Event) -> bool:
        hit = False

        return hit

    def handle_event(self, event:pygame.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == CustomEvent.TO_UI:
            if event.ui_action == "close":
                self.teardown_ui()
            elif event.ui_action == "open":
                self.setup_ui()
            return

        for interactable in self.all_interactables:
            hit = interactable.process_event(event)
            if hit:
                return
        
        hit = self._handle_ui_event(event)
        if hit:
            return
        
        self.current_room.handle_event(event)

        
        


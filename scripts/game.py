import scripts.rooms.room as r
from scripts.rooms.startroom import StartRoom
from scripts.rooms.room1 import Room1
from scripts.fonts import Fonts
import pygame
from scripts.interactable import Interactable
from scripts.button import Button
from scripts.custiom_events import CustomEvent
from scripts.layeredsprite import LayeredSprite
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
    def room_sprites(self) -> pygame.sprite.Group:
        return self.current_room.all_sprites
        
    def draw(self, pixel_screen: pygame.Surface):
        self.current_room.draw(pixel_screen)
        self.ui_sprites.draw(pixel_screen)

    def update_all_sprites(self) -> pygame.sprite.Group:
        all_sprites = self.get_all_sprites()
        all_sprites.update()
        return self.get_all_sprites()
        
    def change_room(self, new_room_key:str):
        if self.current_room is not None:
            self.current_room.teardown()
        self.current_room = self.rooms[new_room_key]()
        self.current_room.setup()

    def update(self):
        self.ui_sprites.update()
        self.room_sprites.update()

    def handle_mouselocation(self, mouseLocation:tuple):
        
        hit = False
        for interactable in self.ui_sprites:
            try:
                hit = interactable.check_hover_state(mouseLocation)
            except AttributeError:
                pass
            if hit:
                return
        
        for interactable in self.room_sprites:
            try:
                hit = interactable.check_hover_state(mouseLocation)
            except AttributeError:
                pass
            if hit:
                return

    def setup_ui(self):
        if self.ui_open:
            return
        
        theme = {
            "background":  "#632908FF",
        }
        self.speak_box = LayeredSprite(pygame.Rect(10, 264, 522, 90), self.ui_sprites, layer=0,
                                       theme=theme, id="speak_box")


        self.ui_open = True

    def teardown_ui(self):
        if not self.ui_open:
            return
        
        for sprite in self.ui_sprites:
            sprite.kill()
        
        self.ui_open = False

    def _handle_ui_event(self, event:pygame.Event) -> bool:
        hit = False

        return hit

    def handle_event(self, event:pygame.Event):
        hit = False
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == CustomEvent.TO_UI:
            if event.action == "close":
                self.teardown_ui()
            elif event.action == "open":
                self.setup_ui()
            return
        
        # Processing Clicks, turns them into click events. 
        for interactable in self.ui_sprites:
            try:
                hit = interactable.process_event(event)
            except AttributeError:
                pass
            if hit:
                return
        for interactable in self.room_sprites:
            try:
                hit = interactable.process_event(event)
            except AttributeError:
                pass
            if hit:
                return
        
        # Handling Events generated above....
        hit = self._handle_ui_event(event)
        if hit:
            return
        
        if event.type == CustomEvent.CHANGE_ROOM:
            self.change_room(event.room)
            return
        
        self.current_room.handle_event(event)

        
        


import scripts.rooms.room as r
from scripts.rooms.startroom import StartRoom
from scripts.fonts import Fonts
import pygame
from scripts.interactable import Interactable
from scripts.button import Button
import random

"""
Holds all info regarding the game-state. 
"""
class Game:
    
    def __init__(self):
        #Start Class Variables

        self.i = 0
        self.rooms = {
            "start_room": StartRoom
        }
        self.inventory = []
        self.current_room:r = None
        self.change_room("start_room")
        
        return

    """Loads game from file"""
    def load_game(self) -> None:
        print("Loading not implemented")
        return

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

    def handle_event(self, event:pygame.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        for interactable in self.all_interactables:
            hit = interactable.process_event(event)
            if hit:
                return
            
        self.current_room.handle_event(event)

        
        


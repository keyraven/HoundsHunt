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
        self.rooms = [StartRoom()]
        self.inventory = []
        self.current_room_index = 0

        return

    """Loads game from file"""
    def load_game(self) -> None:
        print("Loading not implemented")
        return

    @property
    def current_room(self) -> r.Room:
        return self.rooms[self.current_room_index]
    
    def draw(self, pixel_screen: pygame.Surface):
        self.current_room.draw(pixel_screen)

    @property 
    def all_sprites(self) -> pygame.sprite.Group:
        return self.current_room.all_sprites
    
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
    
    def preprocess_events(self):
        pass
        

    """
    Given the x,y position of the click, processes the click and makes changes. 
    """
    def process_click(self, pos: tuple) -> None:
        for spr in self.all_sprites:
            if spr.rect.collidepoint(pos):
                spr.when_interacted()

    """
    Process some keydown. 
    """
    def process_keypress(self) -> None: 
        return
    
    def test_interaction(self, print_string):
        self.i += 1
        print("Interaction!!!!!!", print_string, self.i)

    def test_create_interactable(self):
        test = Interactable(pygame.rect(0,3,4,6),  lambda: self.test_interaction("new string"))
    


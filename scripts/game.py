import scripts.rooms.room as r
from scripts.rooms.startroom import StartRoom
from scripts.rooms.room1 import Room1
from scripts.fonts import Fonts
import pygame
from scripts.interactable import Interactable
from scripts.button import Button
from scripts.custiom_events import CustomEvent
from scripts.layeredsprite import LayeredSprite
from scripts.textbox import TextBox
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
        self.active_item = None
        self.current_room:r = None
        self.change_room("start_room")
        
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.ui_open = False

        self.speak_stack = []
        self.speak_index = 0
        self.speak_box_hitbox = None
        
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
        """Allows objects to react to hover """
        
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

    def update_speak_theme(self, new_theme):

        if new_theme == "hound":
            theme = {
                "dark_box": "#363020",
                "light_box": "#605C4E",
                "text_color": "#000000",
                "photo_background": "#A49966"
            }

            font = Fonts.preview_20
            photo = pygame.image.load("resources/UI/hound-face.png")

        else:
            theme = {
                "dark_box": "#363020",
                "light_box": "#605C4E",
                "text_color": "#000000",
                "photo_background": "#36302000"
            }

            font = Fonts.preview_20
            photo = None
            

        self.speak_box.update_theme(
            {
                "background": theme["dark_box"]
            }
        )
        self.speak_box_inner.update_theme(
            {
                "background": theme["light_box"]
            }
        )
        self.speak_text_box.update_theme(
            {
                "text_color": theme["text_color"]
            }
        )
        self.speak_text_box.text_renderer = font

        self.picture.update_theme(
            {
                "background": theme["photo_background"]
            }
        )
        self.picture.update_image(photo)

    def set_speak_visablity(self, visable:bool):
        """Sets the speak box visablity."""
        if not self.ui_open:
            return

        self.speak_box.visible = visable
        self.speak_box_inner.visible = visable
        self.speak_text_box.visible = visable
        self.picture.visible = visable
        self.speak_text_box.visible = visable
        self.speak_box_hitbox.visible = visable

    def setup_ui(self, theme = "default"):
        if self.ui_open:
            return
        
        l = 0
        
        # SETUP SPEECH BOX  ------------------------------------------------------------------------
        self.speak_box = LayeredSprite(pygame.Rect(10, 264, 522, 90), self.ui_sprites, layer=l,
                                       id="speak_box", visible=False)
        l += 1

        border_size = 3
        self.speak_box_inner = LayeredSprite(pygame.Rect(10+border_size, 264+border_size, 522-2*border_size, 90-2*border_size), 
                                             self.ui_sprites, layer=l, id="speak_box_inner", visible=False)
        
        l += 1
        self.picture = LayeredSprite(pygame.Rect(20, 273, 85, 74), self.ui_sprites, layer=l,
                                       id="picture", visible=False)
        
        self.speak_text_box = TextBox(pygame.Rect(107, 273, 416, 73), "", None, groups = self.ui_sprites, 
                                      layer=l, antialias=False, visible=False, animate=True)
        
        l += 1
        
        self.speak_box_hitbox = Interactable(pygame.Rect(10, 264, 522, 90), self.ui_sprites, layer=l,
                                              id="speak_hitbox", visible=False)

        self.update_speak_theme(theme)

        # SETUP INVENTORY BOX: 

        theme = {
            "background":  "#363020",
        }
        self.inventory_box = LayeredSprite(pygame.Rect(540, 264, 90, 90), self.ui_sprites, theme=theme)
        
        border_size = 3
        theme = {
            "background":  "#605C4E",
        }
        self.inventory_box_inner = LayeredSprite(pygame.Rect(540+border_size, 264+border_size, 90-2*border_size, 90-2*border_size), 
                                                 self.ui_sprites, theme=theme)
        
        self.ui_open = True

    def teardown_ui(self):
        if not self.ui_open:
            return
        
        for sprite in self.ui_sprites:
            sprite.kill()
        
        self.ui_open = False

    def proceed_speak(self) -> bool:
        """Proceeds the speak stack. If there is nothing to proceed, hide the speak box and return True. """
        if self.speak_index >= len(self.speak_stack):
            self.speak_index = 0
            self.speak_stack = []
            self.set_speak_visablity(False)
            return True

        self.set_speak_visablity(True)
        self.speak_text_box.set_text(self.speak_stack[self.speak_index][1])
        self.update_speak_theme(self.speak_stack[self.speak_index][0])
        self.speak_index += 1
        return False

    def _handle_ui_event(self, event:pygame.Event) -> bool:
        hit = False

        if event.type == CustomEvent.BUTTON_KEYDOWN:
            if event.sprite == self.speak_box_hitbox:
                hit = True
                if not self.speak_text_box.animation_over(): 
                    self.speak_text_box.end_animation()
                else:
                    if self.proceed_speak():
                        pygame.event.post(pygame.event.Event(CustomEvent.FROM_UI, {"action": "speak_over"}))

        return hit
    
    def _handle_ui_signaling(self, event:pygame.Event):
        if event.type == CustomEvent.TO_UI:
            if event.action == "speak":
                self.speak_stack = event.data
                self.speak_index = 0
                self.proceed_speak()
            elif event.action == "close":
                self.teardown_ui()
            elif event.action == "open":
                self.setup_ui()
        elif event.type == CustomEvent.CHANGE_ROOM:
            self.change_room(event.room)
        
    def handle_events(self):

        # Start by processing raw events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            hit = self._process_event(event)
            if hit:
                continue

        #Then, process events developed above
        for event in pygame.event.get():
            hit = self._handle_ui_event(event)
            if hit:
                continue
            
            hit = self.current_room.handle_event(event, self.active_item)
            if hit:
                continue
        
        # Then, process UI signals raised above, until there are none left. 
        while True:
            for event in pygame.event.get():
                self.current_room.handle_ui_signals(event, self.active_item)
                self._handle_ui_signaling(event)

            if not pygame.event.peek():
                break
                
              
    def _process_event(self, event:pygame.Event):
        for interactable in self.ui_sprites:
            try:
                hit = interactable.process_event(event)
            except AttributeError:
                pass
            if hit:
                return True
        for interactable in self.room_sprites:
            try:
                hit = interactable.process_event(event)
            except AttributeError:
                pass
            if hit:
                return True
        
        return False
        
        
        

        
        


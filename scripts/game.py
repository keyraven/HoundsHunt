import scripts.rooms.room as r
from scripts.rooms.startroom import StartRoom
from scripts.rooms.room1 import Room1
from scripts.rooms.room2 import Room2
from scripts.fonts import Fonts
import pygame
from scripts.interactable import Interactable
from scripts.button import Button
from scripts.custiom_events import CustomEvent
from scripts.layeredsprite import LayeredSprite
from scripts.textbox import TextBox
from scripts.inventoryobject import InventoryObject
from math import ceil

"""
Holds all info regarding the game-state. 
"""
class Game:
    
    def __init__(self):
        #Start Class Variables

        self.i = 0
        self.rooms = {
            "start_room": StartRoom,
            "room1": Room1,
            "room2": Room2,
        }
        self.inventory = []
        self.active_item = None
        self.current_room:r = None
        self.change_room("start_room")
        
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.ui_open = False
        self.inventory_open = False

        self.speak_stack = []
        self.speak_index = 0
        
        # Interactables
        self.speak_box_hitbox = None
        self.inventory_expand_button = None
        self.inventory_compact_button = None
        self.inventory_scroll_down = None
        self.inventory_scroll_up = None
        
        #UI Parameters:
        self.inventory_page = 0

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
        for interactable in self.ui_sprites.sprites()[::-1]:
            if hit:
                try:
                    interactable.set_hover_state(False)
                except AttributeError:
                    pass
                continue

            try:
                hit = interactable.set_hover_state_from_pos(mouseLocation)
            except AttributeError:
                pass

        hit = False
        for interactable in self.room_sprites.sprites()[::-1]:
            if hit:
                try:
                    interactable.set_hover_state(False)
                except AttributeError:
                    pass
                continue

            try:
                hit = interactable.set_hover_state_from_pos(mouseLocation)
            except AttributeError:
                pass
            

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
        self.inventory_box_image = LayeredSprite(pygame.Rect(540+border_size, 264+border_size, 90-2*border_size, 80), 
                                                 self.ui_sprites)
        
        
        
        theme = {
            "shape": "poly((0,20)(60,20)(30,0))",
            "background": "#363020",
            "hover_background": "#605C4E"
        }
        self.inventory_expand_button = Interactable(pygame.Rect(555, 240, 60, 20), self.ui_sprites, theme=theme, collide_on_vis=True)
        
        self.ui_open = True


        theme = {
            "background": "#302C1F",
        }
        self.inventory_background = LayeredSprite(pygame.Rect(540, 13, 90, 251), self.ui_sprites, theme=theme, visible=False)
        
        theme = {
            "background": "#A49966",
            "hover_background": "#DBCC8B"
        }
        self.inventory_compact_button = Interactable(pygame.Rect(620, 10, 13, 13), self.ui_sprites, theme=theme, visible=False, layer = 5)

        theme = {
            "background": "#605C4E",
            "hover_background": "#79735E",
            "disabled_background": "#72716E"
        }
        self.inventory_slot_backgrounds = [Interactable(pygame.Rect(545, 17, 80, 80), self.ui_sprites, theme=theme, layer=1, visible=False),
                                           Interactable(pygame.Rect(545, 100, 80, 80), self.ui_sprites, theme=theme, layer=1, visible=False),
                                           Interactable(pygame.Rect(545, 183, 80, 80), self.ui_sprites, theme=theme, layer=1, visible=False)]
        
        for x in self.inventory_slot_backgrounds:
            x.send_hover_events = True

        theme = {
            "glow" : "#FFFFFF",
            "glow_radius": 1,
            "text_color": "#000000",
            "horizontal_alignment": "center",
            "vertical_alignment": "center"
        }
        self.inventory_object_names = [TextBox(pygame.Rect(545, 17, 80, 80), "", Fonts.mont_heavy_15, self.ui_sprites, layer=3, theme=theme, antialias=False, visible=False),
                                       TextBox(pygame.Rect(545, 100, 80, 80), "", Fonts.mont_heavy_15, self.ui_sprites, layer=3, theme=theme, antialias=False, visible=False),
                                       TextBox(pygame.Rect(545, 183, 80, 80), "", Fonts.mont_heavy_15, self.ui_sprites, layer=3, theme=theme, antialias=False, visible=False)]

        self.inventory_images = [LayeredSprite(pygame.Rect(545, 17, 80, 80), self.ui_sprites, layer=2, visible=False),
                                 LayeredSprite(pygame.Rect(545, 100, 80, 80), self.ui_sprites, layer=2, visible=False),
                                 LayeredSprite(pygame.Rect(545, 183, 80, 80), self.ui_sprites, layer=2, visible=False)]
        

        theme = {
            "shape": "poly((0,10)(40,10)(20,0))",
            "background": "#363020",
            "hover_background": "#93803E",
            "disabled_background": "#1B1911",
        }
        self.inventory_scroll_up = Interactable(pygame.Rect(565, 19, 40, 10), self.ui_sprites, layer=3, theme=theme, visible=False, collide_on_vis=True)
        theme = {
            "shape": "poly((0,0)(40,0)(20,10))",
            "background": "#363020",
            "hover_background": "#93803E",
            "disabled_background": "#1B1911",
        }
        self.inventory_scroll_down = Interactable(pygame.Rect(565, 251, 40, 10), self.ui_sprites, layer=3, theme=theme, visible=False, collide_on_vis=True)


        self.update_draw_inventory()

        # Inventory Close Look
        theme = {
            "background": "#302C1F",
        }
        self.inventory_close_look_background = LayeredSprite(pygame.Rect(195, 30, 390, 230), self.ui_sprites, visible=False)

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

        if event.type == CustomEvent.BUTTON_KEYDOWN:
            if event.sprite == self.speak_box_hitbox:
                if not self.speak_text_box.animation_over(): 
                    self.speak_text_box.end_animation()
                else:
                    if self.proceed_speak():
                        pygame.event.post(pygame.event.Event(CustomEvent.FROM_UI, {"action": "speak_over"}))
            elif event.sprite == self.inventory_expand_button:
                self.inventory_page = 0
                self.set_inventory_visablity(True)
            elif event.sprite == self.inventory_compact_button:
                self.set_inventory_visablity(False)
            elif event.sprite == self.inventory_scroll_down:
                self.inventory_page += 1
                self.update_draw_inventory()
            elif event.sprite == self.inventory_scroll_up:
                self.inventory_page -= 1
                self.update_draw_inventory()

        elif event.type == CustomEvent.BUTTON_HOVER:
            try:
                index = self.inventory_slot_backgrounds.index(event.sprite)
            except ValueError:
                pass
            else:
                self.inventory_object_names[index].visible = True
        elif event.type == CustomEvent.BUTTON_UNHOVER:
            try:
                index = self.inventory_slot_backgrounds.index(event.sprite)
            except ValueError:
                pass
            else:
                self.inventory_object_names[index].visible = False
        elif event.type == CustomEvent.TO_UI:
            if event.action == "speak":
                hit = True
                self.speak_stack = event.data
                self.speak_index = 0
                self.proceed_speak()
            elif event.action == "close":
                hit = True
                self.teardown_ui()
            elif event.action == "open":
                hit = True
                self.setup_ui()
            elif event.action == "add_inventory":
                self.add_to_inventory(event.object)
                self.update_draw_inventory()
            elif event.action == "remove_inventory":
                self.remove_from_inventory(event.object)
                self.update_draw_inventory()

        return
    
    def handle_event(self, event:pygame.Event):
        """First Stop for Events. Calls other event handlers. """
        
        hit = False
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
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
        self._handle_ui_event(event)
        
        if event.type == CustomEvent.CHANGE_ROOM:
            self.change_room(event.room)
            return
        
        self.current_room.handle_event(event, self.active_item)

    def set_inventory_visablity(self, visablity):      
        self.inventory_open = visablity

        self.inventory_expand_button.visible = not visablity
        self.inventory_background.visible = visablity
        self.inventory_compact_button.visible = visablity
        self.inventory_scroll_up.visible = visablity
        self.inventory_scroll_down.visible = visablity
        for object in self.inventory_slot_backgrounds:
            object.visible = visablity
        for object in self.inventory_images:
            object.visible = visablity
        
        self.update_draw_inventory()

    def add_to_inventory(self, new_object:InventoryObject):
        if type(new_object) is not InventoryObject:
            print(f"Tried to add \"{new_object}\" to inventory, but it's not an inventory object.")
            return
        
        self.inventory.append(new_object)
        if len(self.inventory) == 1:
            self.active_item = new_object

    def remove_from_inventory(self, remove_object):
        """Takes ID or InventoryObject"""

        if type(remove_object) is str:
            for object in self.inventory:
                if remove_object == object.id:
                    remove_object = object
                    break
            else:
                return
        
        if remove_object in self.inventory:
            self.inventory.remove(remove_object)
        else:
            return
        
        if remove_object == self.active_item:
            self.active_item = None

        self.update_draw_inventory()

    def update_draw_inventory(self):
        if not self.ui_open:
            return

        if self.active_item is None:
            self.inventory_box_image.update_image(LayeredSprite.empty_surface)
        else:
            self.inventory_box_image.update_image(self.active_item.image)
        
        if not self.inventory_open:
            return
        
        max_page = ceil(len(self.inventory) / 3)
        if self.inventory_page > max_page:
            self.inventory_page = max_page
        elif self.inventory_page < 0:
            self.inventory_page = 0

        self.inventory_scroll_up.disabled = self.inventory_page <= 0
        self.inventory_scroll_down.disabled = self.inventory_page >= max_page - 1


        for i in range(0, 3):
            try:
                inventory_object = self.inventory[i + self.inventory_page*3]
            except IndexError:
                self.inventory_slot_backgrounds[i].disabled = True
                self.inventory_images[i].update_image(LayeredSprite.empty_surface)
                self.inventory_object_names[i].set_text("")
                self.inventory_slot_backgrounds[i].id = None
                continue

            self.inventory_slot_backgrounds[i].disabled = False
            self.inventory_images[i].update_image(inventory_object.image)
            self.inventory_object_names[i].set_text(inventory_object.name)
            self.inventory_slot_backgrounds[i].id = inventory_object # Not ideal.  HACKY
        
# Utility Functions
from scripts.rooms.room import Room, View
import pygame
from scripts.custiom_events import CustomEvent
from scripts.animatedinteractable import AnimatedInteractable
from scripts.interactable import Interactable
from scripts.inventoryobject import InventoryObject


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
        view1.left = view4
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
        self.lookindown = View(lookin_background, 6, build_function=Room2.build_lookindown)
        self.lookindown.up = view1

        lookin_background = pygame.image.load("resources/room2/nut_lookin.png")
        self.nut_lookin = View(lookin_background, 7, build_function=Room2.build_nut_lookin)
        self.nut_lookin.up = view2

        lookin_background = pygame.image.load("resources/room2/eye_lookin.png")
        self.eye_lookin = View(lookin_background, 8, build_function=Room2.build_eye_lookin)
        self.eye_lookin.up = view4

        lookin_background = pygame.image.load("resources/room2/rock_lookin.png")
        self.rock_lookin = View(lookin_background, 9, build_function=Room2.build_rock_lookin)
        self.rock_lookin.down = view3


        view1.down = self.lookindown
        view2.down = self.lookindown
        view3.down = self.lookindown
        view4.down = self.lookindown

        self._current_view = view1
        self._current_view.show()

        # Send opening event
        event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You break from the rift, and find yourself in a strange, uncanny desert."),
                                                                                 ("hound", "HOUND: Now... where is my prey?"), 
                                                                                 ("hound", "HOUND: I cannot sense it's mind. The trail has gone cold."),
                                                                                 ("None", "Perhaps, if your prey left something behind, their mind would be revealed to you.")],
                                                                "echo": 1})
        pygame.event.post(event)
        self.disable_room = True #Disable Room Until Starting Dialouge is over


        # Puzzles
        self.corect_ground_seq = ["hook", "quad", "hexagon", "circle", "triangle", "hexagon"]
        self.ground_seq_number = 0
        self.ground_puzzle_completed = False
        self.eyes_cry = False
    
    def draw(self, draw_surface):
        draw_surface.blit(self.current_view.background, (0,0))
        super().draw(draw_surface)

    @Room.current_view.setter
    def current_view(self, value):
        if value != self.lookindown:
            self.lookindown.up = value
        self.ground_seq_number = 0
        super(Room2, type(self)).current_view.fset(self, value)

    def handle_event(self, event, active_item=None):
        # Handle Disabling... 
        if event.type == CustomEvent.FROM_UI:
            if event.action == "speak_over":
                self.disable_room = False
                if event.echo == "win":
                    event = pygame.Event(CustomEvent.CHANGE_ROOM, {"room": "start_room"})
                    pygame.event.post(event)

                    event = pygame.Event(CustomEvent.TO_UI, {"action": "close"})
                    pygame.event.post(event)

        if self.disable_room:
            return

        # Handle Changing View
        change_view = None
        if self.current_view is not None:
            change_view = self.current_view.handle_arrow_event(event)
        if change_view is not None:
            self.current_view = change_view

        #VIEW EVENTS
        if self.current_view.id == 1:
            self.handle_view_1_events(event, active_item)
        elif self.current_view.id == 2:
            self.handle_view_2_events(event, active_item)
        elif self.current_view.id == 3:
            self.handle_view_3_events(event, active_item)
        elif self.current_view.id == 4:
            self.handle_view_4_events(event, active_item)
        elif self.current_view.id == 5:
            self.handle_lookinview_2_events(event, active_item)
        elif self.current_view.id == 6:
            self.handle_lookindown_events(event, active_item)
        elif self.current_view.id == 7:
            self.handle_nut_lookin_events(event, active_item)
        elif self.current_view.id == 8:
            self.handle_eye_lookin_events(event, active_item)
        elif self.current_view.id == 9:
            self.handle_rock_lookin_events(event, active_item)

    def handle_view_1_events(self, event, active_item=None):
        return

    def handle_view_2_events(self, event, active_item=None):
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "tree_lookin":
                self.current_view = self.lookinview2
            elif event.sprite.id == "open_nut":
                self.current_view = self.nut_lookin

    def handle_nut_lookin_events(self, event, active_item=None):

        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "glass":
                event.sprite.kill()
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("blue_glass", "Dirty Glass Shard", 
                                                                                                                image=pygame.image.load("resources/objects/glass.png"))})
                
                pygame.event.post(event)


                event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You pick up a dirty shard of glass.")],
                                                                "echo": 1})
                pygame.event.post(event)
                self.disable_room = True
            elif event.sprite.id == "red_powder":
                event.sprite.kill()
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("red_powder", "Red Powder", 
                                                                                                                image=pygame.image.load("resources/objects/red_powder.png"))})
                
                pygame.event.post(event)


                event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You pick up a small pile of red dust."),
                                                                                         ("None", "A few grains blow into your eyes, irritating and painfull.")],
                                                                "echo": 1})
                pygame.event.post(event)
                self.disable_room = True
   
    def handle_view_3_events(self, event, active_item=None):
        
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "rock_small":
                self.current_view = self.rock_lookin
    
    def handle_view_4_events(self, event, active_item=None):
        
        if event.type == CustomEvent.BUTTON_KEYDOWN:
            if event.sprite.id == "blink":
                self.current_view = self.eye_lookin
    
    def handle_lookinview_2_events(self, event, active_item=None):
        
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "nut":
                event.sprite.kill()

                event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "The nut falls to the ground.")],
                                                                "echo": 2})
                self.current_view.down.background = pygame.image.load("resources/room2/view2_2.png")
                # hate this
                
                theme = {
                    "image": pygame.image.load("resources/room2/open_nut.png")
                }
                Interactable(pygame.Rect(305, 263, 76, 51), self.current_view.down.all_sprites, theme=theme, id = "open_nut")


                self.disable_room = True
                pygame.event.post(event)

    def handle_lookindown_events(self, event, active_item=None):
        
        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id in self.corect_ground_seq and not self.ground_puzzle_completed:
                if event.sprite.id == self.corect_ground_seq[self.ground_seq_number]:
                    self.ground_seq_number += 1
                    print("CORRECT")
                else:
                    self.ground_seq_number = 0
                
                if self.ground_seq_number >= len(self.corect_ground_seq):
                    self.complete_hexagon_puzzle()

        if event.type == CustomEvent.FROM_UI:
            if event.action == "speak_over" and event.echo == 1:
                self.disable_room = False


            event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("dirty_blue_gem", "Dirty Blue Stone", 
                                                                                                                image=pygame.image.load("resources/objects/dirty_blue_gem.png"))})
            pygame.event.post(event)

    def handle_eye_lookin_events(self, event, active_item=None):

        if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "blink_close":
                if active_item and active_item.id == "red_powder" and not self.eyes_cry:
                    
                    theme = {
                        "image": pygame.image.load("resources/room2/tears.png")
                    }
                    Interactable(pygame.Rect(149, 214, 232, 124), self.current_view.all_sprites, theme=theme, id = "tears")
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You blow the red dust into the eyes. Silently, they began to cry.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)

                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"remove_inventory", "object": "red_powder"})
                    pygame.event.post(event)

                    self.eyes_cry = True
                elif self.eyes_cry:
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "The eyes cry, but they stare still.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)
                else:
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "The eyes stare.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)
            elif event.sprite.id == "tears":
                if active_item and active_item.id == "blue_glass":
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You clean the glass in the strange tears.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)

                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"remove_inventory", "object": "blue_glass"})
                    pygame.event.post(event)

                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"add_inventory", "object": InventoryObject("clean_glass", "Clean Glass Shard", 
                                                                                                                       image=pygame.image.load("resources/objects/glass_clean.png"))})
                    pygame.event.post(event)
    
    def handle_rock_lookin_events(self, event, active_item=None):
         if event.type == CustomEvent.BUTTON_KEYUP:
            if event.sprite.id == "large_rock":
                if active_item and active_item.id == "clean_glass":
                    event1 = pygame.event.Event(CustomEvent.TO_UI, {"action":"remove_inventory", "object": "clean_glass"})
                    pygame.event.post(event1)

                    event1 = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You look through the glass, and deep carvings appear.")], "echo": None})
                    self.disable_room = True

                    event.sprite.update_theme({"image": pygame.image.load("resources/room2/carved_rock.png")})
                    pygame.event.post(event1)
                elif active_item and active_item.id == "blue_glass":
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "You can almost see something through the glass... but it's too dirty.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)
                else:
                    event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "A large rock.")], "echo": None})
                    self.disable_room = True
                    pygame.event.post(event)

    def build_view_1(all_sprites):
        return
    
    def build_view_2(all_sprites):
        
        # Interactable to enter into the close-view tree look
        theme = {
            #"background": "black"
        }
        Interactable(pygame.Rect(312, 63, 108, 157), all_sprites, theme=theme, id="tree_lookin")
          
    def build_view_3(all_sprites):
        
        theme = {
            "image": pygame.image.load("resources/room2/rock_small.png")
        }
        Interactable(pygame.Rect(230, 241, 126, 49), all_sprites, theme=theme, collide_on_vis=True, id="rock_small")
    
    def build_view_4(all_sprites):
        
        frames, mask = AnimatedInteractable.get_frames_dir("resources/eye_blink")
        AnimatedInteractable(pygame.Rect(431, 234, 19, 23), frames, all_sprites, delay=200, id="blink", speed=20)
    
    def build_lookinview_2(all_sprites):
        
        theme = {
            "image": pygame.image.load("resources/room2/coconut.png")
        }
        Interactable(pygame.Rect(133, 159, 105, 133), all_sprites, theme=theme, id="nut")
    
    def build_lookindown(all_sprites):
        
        theme = {
            "image": pygame.image.load("resources/room2/ground_hexagon.png"),
            "hover_image":pygame.image.load("resources/room2/ground_hexagon_hover.png"),
            #"active_image": pygame.image.load("resources/room2/ground_hexagon.png"),
            #"background": "black"
        }
        Interactable(pygame.Rect(251, 146, 183, 112), all_sprites, theme=theme, collide_on_vis=True, 
                     id = "hexagon")
        
        theme = {
            "image": pygame.image.load("resources/room2/ground_hook.png"),
            "hover_image":pygame.image.load("resources/room2/ground_hook_hover.png"),
            #"active_image": pygame.image.load("resources/room2/ground_hook.png"),
            #"background": "black"
        }
        Interactable(pygame.Rect(121, 83, 159, 55), all_sprites, theme=theme, collide_on_vis=True, 
                     id = "hook")
        
        theme = {
            "image": pygame.image.load("resources/room2/ground_triangle.png"),
            "hover_image":pygame.image.load("resources/room2/ground_triangle_hover.png"),
            #"active_image": pygame.image.load("resources/room2/ground_triangle.png"),
            #"background": "black"
        }
        Interactable(pygame.Rect(71, 51, 74, 16), all_sprites, theme=theme, collide_on_vis=True, 
                     id = "triangle")
        
        theme = {
            "image": pygame.image.load("resources/room2/ground_circle.png"),
            "hover_image":pygame.image.load("resources/room2/ground_circle_hover.png"),
            #"active_image": pygame.image.load("resources/room2/ground_circle.png"),
            #"background": "black"
        }
        Interactable(pygame.Rect(78, 274, 128, 49), all_sprites, theme=theme, collide_on_vis=True, 
                     id = "circle")
        
        theme = {
            "image": pygame.image.load("resources/room2/ground_quad.png"),
            "hover_image":pygame.image.load("resources/room2/ground_quad_hover.png"),
            #"active_image": pygame.image.load("resources/room2/ground_quad.png"),
            #"background": "black"
        }
        Interactable(pygame.Rect(415, 69, 130, 48), all_sprites, theme=theme, collide_on_vis=True, 
                     id = "quad")
        
    def build_nut_lookin(all_sprites):
        
        theme = {
            "image": pygame.image.load("resources/room2/glass.png")
        }
        Interactable(pygame.Rect(188, 143, 140, 89), all_sprites, theme=theme, id = "glass")

        theme = {
            "image": pygame.image.load("resources/room2/red_powder.png")
        }
        Interactable(pygame.Rect(285, 213, 59, 29), all_sprites, theme=theme, id = "red_powder", layer=2)
    
    def build_eye_lookin(all_sprites):
        
        frames, mask = AnimatedInteractable.get_frames_dir("resources/eye_blink_close")
        AnimatedInteractable(pygame.Rect(151, 198, 72, 32), frames, all_sprites, delay=200, id="blink_close", speed=20)

    def build_rock_lookin(all_sprites):
        
        theme = {
            "image": pygame.image.load("resources/room2/plain_rock.png")
        }
        Interactable(pygame.Rect(134, 138, 470, 186), all_sprites, theme=theme, collide_on_vis=True, id = "large_rock")

    def complete_hexagon_puzzle(self):
        self.ground_puzzle_completed = True
        self.ground_seq_number = 0  

        self.disable_room = True
        
        event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("None", "The ground begins to quake and shiver strangly. You take a cautious step back"),
                                                                                 ("None", "Slowly, almost painfully, a handgun emerges from the cracked earth."), 
                                                                                 ("None", "As gently as your claws allow, you pick it up."),
                                                                                 ("hound", "Yes... This play-toy belonged to my prey. I can feel the fear on it."),
                                                                                 ("None", "From the handgun, you catch the scent of your prey, and continue the hunt."),
                                                                                 ("None", "Soon, you track down the pray, and feast.")],
                                                                "echo": "win"})
        pygame.event.post(event)

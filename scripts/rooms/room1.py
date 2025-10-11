from scripts.rooms.room import Room
import pygame
from scripts.custiom_events import CustomEvent
from scripts.animatedinteractable import AnimatedInteractable
from scripts.inventoryobject import InventoryObject

class Room1(Room):

    def __init__(self):
        super().__init__()

        self.background = pygame.image.load("./resources/room1.png")

    def setup(self):
        #Send Signal to Open UI
        pygame.event.post(pygame.event.Event(CustomEvent.TO_UI, {"action": "open"}))

        (glitter_frames, glitter_mask) = AnimatedInteractable.get_frames_dir("resources/glitter_animation")

        self.glitter = AnimatedInteractable(pygame.Rect(175, 32, glitter_frames[0].get_width(), glitter_frames[0].get_height()), 
                                             glitter_frames, self.all_sprites, speed = 10, hover_speed = 6, 
                                             mask=glitter_mask)

    def draw(self, draw_surface):
        draw_surface.blit(self.background, (0,0))
        super().draw(draw_surface)

    def handle_event(self, event, active_item=None):
        super().handle_event(event, active_item)

        if event.type == CustomEvent.BUTTON_KEYDOWN:
            if event.sprite == self.glitter:

                event = pygame.event.Event(CustomEvent.TO_UI, {"action":"speak", "data":[("hound", "HOUND: What is this? Something moves beyond the veil. "), 
                                                                                            (None, "(hunger drives you forward. you rip open the rift, and throw yourself inward)")],
                                                                "echo": 1})
                pygame.event.post(event)


                """### TEST TEST TEST
                image = pygame.image.load("resources/objects/test.png")
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("test1", "Test 1", image=image)})
                pygame.event.post(event)
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("test2", "Test 2", image=image)})
                pygame.event.post(event)
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("test3", "Test 3", image=image)})
                pygame.event.post(event)
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("test4", "Test 4", image=image)})
                pygame.event.post(event)
                event = pygame.event.Event(CustomEvent.TO_UI, {"action": "add_inventory", "object": InventoryObject("test4", "Test 4", image=image)})
                pygame.event.post(event)
                """
                
        elif event.type == CustomEvent.FROM_UI:
            if event.action == "speak_over" and event.echo == 1:
                pygame.event.post(pygame.Event(CustomEvent.CHANGE_ROOM, {"room": "room2"}))
from scripts.rooms.room import Room, View
import pygame
from scripts.custiom_events import CustomEvent
from scripts.animatedinteractable import AnimatedInteractable


class Room2(Room):

    def __init__(self):
        super().__init__()

    

    def handle_event(self, event, active_item=None):
        return super().handle_event(event, active_item)
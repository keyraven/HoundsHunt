import pygame

class CustomEvent():
    INTERACT = pygame.event.custom_type()
    BUTTON_KEYDOWN = pygame.event.custom_type()
    BUTTON_KEYUP = pygame.event.custom_type()
    BUTTON_HOTKEY = pygame.event.custom_type()
    BUTTON_HOVER = pygame.event.custom_type()
    TO_UI = pygame.event.custom_type()
    FROM_UI = pygame.event.custom_type()
    CHANGE_ROOM = pygame.event.custom_type()



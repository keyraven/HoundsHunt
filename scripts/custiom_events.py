import pygame

class CustomEvent():
    INTERACT = pygame.event.custom_type()
    BUTTON_KEYDOWN = pygame.event.custom_type()
    BUTTON_KEYUP = pygame.event.custom_type()
    BUTTON_HOTKEY = pygame.event.custom_type()
    BUTTON_HOVER = pygame.event.custom_type()



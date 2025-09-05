import pygame

class Fonts():

    scatched_letters_large:pygame.Font
    preview_large:pygame.Font

    def load_all_fonts():
        Fonts.scatched_letters_large = pygame.Font("resources/font/scratched_letters/Scratched Letters.ttf", 50)
        Fonts.preview_large = pygame.Font("resources/font/preview/Preview.otf", 50)

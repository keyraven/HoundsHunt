import pygame.freetype

class Fonts():

    scatched_letters:pygame.freetype.Font
    preview:pygame.freetype.Font

    def load_all_fonts():
        Fonts.scatched_letters = pygame.freetype.Font("resources/font/scratched_letters/Scratched Letters.ttf", 50)
        Fonts.scatched_letters.antialiased = False
        Fonts.preview = pygame.freetype.Font("resources/font/preview/Preview.otf", 50)
        Fonts.preview.antialiased = False

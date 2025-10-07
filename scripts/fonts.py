import pygame

class Fonts():

    scatched_letters_50:pygame.Font
    
    preview_50:pygame.Font
    preview_20:pygame.Font
    preview_15:pygame.Font
    depixel_halbfett_15:pygame.Font

    def load_all_fonts():
        Fonts.scatched_letters_50 = pygame.Font("resources/font/scratched_letters/Scratched Letters.ttf", 50)

        Fonts.preview_50 = pygame.Font("resources/font/preview/Preview.otf", 50)
        Fonts.preview_20 = pygame.Font("resources/font/preview/Preview.otf", 20)
        Fonts.preview_15 = pygame.Font("resources/font/preview/Preview.otf", 15)
        Fonts.depixel_halbfett_15 = pygame.Font("resources/font/depixel/DePixelHalbfett.ttf", 13)

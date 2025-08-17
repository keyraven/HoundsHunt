import pygame
import scripts.game as game
from scripts.fonts import Fonts

pygame.init()
Fonts.load_all_fonts()

RENDER_RES = (640, 360)
display_screen = pygame.display.set_mode(RENDER_RES, pygame.SCALED)

#Init all the Game Objects, and Such. 
game_info = game.Game()

clock = pygame.time.Clock()

while True: 
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: 
            game_info.process_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            game_info.process_keypress()

        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        

    #Rendering Logic
    game_info.draw_current_room(display_screen)
    game_info.all_sprites.draw(display_screen)
    
    #pygame.transform.scale(pixel_screen, FULL_RES, display_screen) #Scale Pixel Screen to Full Display Resolution
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
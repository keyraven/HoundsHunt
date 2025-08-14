import pygame
import scripts.game as game

pygame.init()

FULL_RES = (1920, 1080)
RENDER_RES = (640, 360)

scale_factors = (RENDER_RES[0]/FULL_RES[0], RENDER_RES[1]/FULL_RES[1])
display_screen = pygame.display.set_mode((FULL_RES))
pixel_screen = pygame.Surface((RENDER_RES))

def adjust_pos(pos:tuple) -> tuple:
    """Adjust position in display resolution to render resolution"""
    return (pos[0] * scale_factors[0], pos[1] * scale_factors[1])

#Init all the Game Objects, and Such. 
game_info = game.Game()

clock = pygame.time.Clock()

while True: 
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: 
            game_info.process_click(adjust_pos(event.pos))

        elif event.type == pygame.KEYDOWN:
            game_info.process_keypress()

        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    pixel_screen.fill("purple")  # Fill the display with a solid color

    #Rendering Logic
    all_sprites = game_info.get_all_sprites()
    all_sprites.update()
    all_sprites.draw(pixel_screen)
    
    pygame.transform.scale(pixel_screen, FULL_RES, display_screen) #Scale Pixel Screen to Full Display Resolution
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
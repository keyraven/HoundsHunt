import sys, platform
import asyncio
import pygame
import scripts.game as game
from scripts.fonts import Fonts

RENDER_RES = (640, 360)

if sys.platform == "emscripten": # Check if the game is running is browser
    #platform.window.canvas.style.imageRendering = "pixelated"
    display_screen = pygame.display.set_mode(RENDER_RES)
    print("Running is Browser!!!")
else:
    print("NOT Running in Browser!!!")
    display_screen = pygame.display.set_mode(RENDER_RES, pygame.SCALED)

pygame.init()
Fonts.load_all_fonts()

#Init all the Game Objects, and Such. 
game_info = game.Game()

clock = pygame.time.Clock()

async def main():
   global RENDER_RES
   global display_screen
   global game_info
   
   

   while True: 
        # Pre-Process Events. 
        game_info.preprocess_events()

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
        game_info.draw(display_screen)
        
        #pygame.transform.scale(pixel_screen, FULL_RES, display_screen) #Scale Pixel Screen to Full Display Resolution
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)
        
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
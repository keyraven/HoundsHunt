import sys, platform
import asyncio
import pygame
import pygame.freetype
import scripts.game as game
from scripts.fonts import Fonts

RENDER_RES = (640, 360)

if sys.platform == "emscripten": 
    # If game is running in browser: 
    platform.window.canvas.style.imageRendering = "pixelated"
    display_screen = pygame.display.set_mode(RENDER_RES)
    print("Running in Browser ~~")
else:
    print("NOT Running in Browser ~~")
    display_screen = pygame.display.set_mode(RENDER_RES, pygame.SCALED)

print("Initializing Pygame...")
pygame.init()
print("Pygame Initialized ...")
Fonts.load_all_fonts()

#Init all the Game Objects, and Such. 
game_info = game.Game()

clock = pygame.time.Clock()

async def main():
   global RENDER_RES
   global display_screen
   global game_info
   
   while True: 
        # Process mouse location
        game_info.handle_mouselocation(pygame.mouse.get_pos())

        # Process player inputs and events. 
        while True:
            for event in pygame.event.get():
                game_info.handle_event(event)
            
            # Events might have been generated above. Check to see if the 
            # event queue if empty, and only proceed if it is. 
            if not pygame.event.peek():
                break
    
        #Stuff to be run every frame
        game_info.update()

        #Rendering Logic
        game_info.draw(display_screen)
        
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)
        
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
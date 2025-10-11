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
        j = 0
        while True:

            i = 0
            for event in pygame.event.get():
                game_info.handle_event(event)
                i += 1
            
            if i == 0:
                break

            j += 1
            """i += 1
            # Events might have been generated above. Check to see if the 
            # event queue if empty, and only proceed if it is. 
            if not pygame.event.peek():
                break"""
            

            # Safety for some weird edge case. 
            # Loops without this worry me. 
            if j > 500:
                print("Too many events per frame!")
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
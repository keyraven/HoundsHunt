from scripts.interactable import Interactable
import pygame
import os 

class AnimatedInteractable(Interactable):

    def __init__(self, rect, frames:list, *groups, hover_frames:list = None, hotkey = None, 
                 layer = 0, repeat:int = -1, speed:int = 1, hover_speed:int = None, theme:dict = None):
        super().__init__(rect, *groups, hotkey=hotkey, layer=layer, theme=theme)

        self.frames = frames
        self.hover_frames = None
        self.i = 0
        self.current_frame = 0
        self.repeat = repeat
        self.speed = speed
        self.hover_speed = hover_speed if hover_speed is not None else self.speed
        self.frame_number = len(frames)
        if hover_frames is not None and len(hover_frames) != len(frames):
            raise ValueError("Need Same Number of Frames in Hover and Normal Animation. ")

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        if self.hover:
            speed = self.hover_speed
            frames = self.hover_frames if self.hover_frames is not None else self.frames
        else:
            speed = self.speed
            frames = self.frames

        self.image = self.get_draw_surface().copy()
        self.image.blit(frames[self.current_frame], (0,0))

        if self.i % speed == 0:
            self.current_frame += 1
            if self.current_frame >= self.frame_number:
                self.current_frame = 0

        self.i += 1

    def get_frames_dir(file_path:str, file_type:str = "png") -> list:
        i = 1
        frames = []

        while True:
            

            try:
                f = pygame.image.load(os.path.join(file_path, f"{i}.{file_type}"))
            except FileNotFoundError:
                break
            
            print(f)

            i += 1
            frames.append(f)

        return frames


            



        



    



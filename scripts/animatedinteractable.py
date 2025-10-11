from scripts.interactable import Interactable
import pygame
import os 

class AnimatedInteractable(Interactable):

    def __init__(self, rect, frames:list, groups = (), hover_frames:list = None, hotkey = None, 
                 layer = 0, repeat:int = -1, speed:int = 1, hover_speed:int = None, theme:dict = None, 
                 mask:pygame.Mask = None, collide_on_vis:bool = False, id = None, visible:bool = True, delay:int = 0):
        super().__init__(rect, groups=groups, hotkey=hotkey, layer=layer, theme=theme, collide_on_vis=collide_on_vis,
                         id=id, visible=visible)

        self.i = 0
        self.current_frame = 0
        self.max_repeats = repeat
        self.repeats = 0
        self.delay = delay
        self.current_delay = delay

        self.speed = speed
        self.hover_speed = hover_speed if hover_speed is not None else self.speed
        if hover_frames is not None and len(hover_frames) != len(frames):
            raise ValueError("Need Same Number of Frames in Hover and Normal Animation. ")
        if type(mask) is list and len(mask) != len(frames):
            raise ValueError("Need same number of frames and masks. Or just one mask. ")

        
        if type(mask) is pygame.Mask:
            self.frames = [self.SurfaceWithMask(i, mask, collide_on_vis) for i in frames]
        elif type(mask) is list:
            self.frames = [self.SurfaceWithMask(i, j, collide_on_vis) for i,j in zip(frames, mask)]
        else:
            self.frames = [self.SurfaceWithMask(i, create_mask=collide_on_vis) for i in frames]

        if hover_frames is None:
            self.hover_frames = None
        elif mask is pygame.Surface:
            self.hover_frames = [self.SurfaceWithMask(i, mask, collide_on_vis) for i in hover_frames]
        elif mask is list:
            self.hover_frames = [self.SurfaceWithMask(i, j, collide_on_vis) for i,j in zip(hover_frames, mask)]
        else:
            self.hover_frames = [self.SurfaceWithMask(i, collide_on_vis) for i in hover_frames]
        
        self._image = None
             

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        if self.hover:
            speed = self.hover_speed
            frames = self.hover_frames if self.hover_frames is not None else self.frames
        else:
            speed = self.speed
            frames = self.frames

        self._image = self.get_draw_surface().copy()
        self._image.blit(frames[self.current_frame].surface, (0,0), lock_mask=True)
        
        if frames[self.current_frame].surface is not None:
            self._image.mask_union(frames[self.current_frame].mask)

        if self.current_delay > 0:
            self.current_delay -= 1
            self.i -= 1 #gross solution. I am tired. 
        elif self.i % speed == 0 and (self.max_repeats < 0 or self.repeats > self.max_repeats):
            self.current_frame += 1
            if self.current_frame >= len(frames):
                self.current_frame = 0
                self.repeats += 1
                self.current_delay = self.delay
        

        self.i += 1

    def restart_animation(self):
        self.repeats = 0

    def get_frames_dir(file_path:str, file_type:str = "png") -> tuple:
        
        frames = []
        mask = None

        i = 1
        while True:
            try:
                f = pygame.image.load(os.path.join(file_path, f"{i}.{file_type}"))
            except FileNotFoundError:
                break

            i += 1
            frames.append(f)

        if os.path.exists(os.path.join(file_path, f"mask.{file_type}")):
            mask = pygame.mask.from_surface(pygame.image.load(os.path.join(file_path, f"mask.{file_type}")))
        
        i = 1
        while True:
            try:
                f = pygame.mask.from_surface(pygame.image.load(os.path.join(file_path, f"mask{i}.{file_type}")))
            except FileNotFoundError:
                break
            
            if mask is None:
                mask = []
            i += 1
            frames.append(f)

        return frames, mask


            



        



    



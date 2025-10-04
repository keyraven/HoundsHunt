from scripts.layeredsprite import LayeredSprite
import pygame

class TextBox(LayeredSprite):

    theme_defaults = {
        "background": "#00000000",
        "text_color": "#000000FF",
        "shape": "rect",
        "y_padding": 0,
        "x_padding": 0,
        "scale_image": False
    }


    def __init__(self, rect, text:str, text_renderer:pygame.Font, groups = (), layer = 0, antialias:bool = True,
                 theme = None, collide_on_vis = False, mask = None, id=None, visible = True,
                 animate = False, animate_speed:int = 8):
        super().__init__(rect, groups=groups, layer=layer, theme=theme, 
                         collide_on_vis=collide_on_vis, mask=mask, id=id, visible=visible)
    
    
        self.text = text
        self.text_renderer = text_renderer
        self.text_color = self.theme.get("text_color", self.theme_defaults["text_color"])
        self.y_padding = self.theme.get("y_padding", self.theme_defaults["y_padding"])
        self.x_padding = self.theme.get("x_padding", self.theme_defaults["x_padding"])
        self.antialias = antialias
        self.animate = animate
        self.animate_speed = animate_speed
        self.i = 0

        if animate:
            self.display_pos = 0
        else:
            self.display_pos = len(self.text)

        self.i = 0

    def set_text(self, new_text):

        self.text = new_text
        if self.animate:
            self.display_pos = 0
        else:
            self.display_pos = len(self.text)

        self.i = 0

    def build_surfaces(self):
        super().build_surfaces()

        if self.text_renderer is not None:
            text_surface, unblited = TextBox.drawText(self.text[:self.display_pos], self.text_color, self.rect, self.text_renderer, self.y_padding, self.x_padding, 
                                        self.antialias)

            self.normal_surface.blit(text_surface)


    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        
        if len(self.text) > self.display_pos:
            self.i += 1
            if self.i % self.animate_speed == 0:
                self.display_pos += 1
                self.build_surfaces()

    def end_animation(self):

        self.display_pos = len(self.text)
        self.build_surfaces()

    def animation_over(self):

        if self.animate:
            if self.display_pos >= len(self.text):
                return True
            else:
                return False

        return True

    def update_theme(self, new_theme:dict):
        super().update_theme(new_theme)

        self.y_padding = self.theme.get("y_padding", self.theme_defaults["y_padding"])
        self.x_padding = self.theme.get("x_padding", self.theme_defaults["x_padding"])
        self.text_color = self.theme.get("text_color", self.theme_defaults["text_color"])


    def drawText(text:str, color, rect:pygame.Rect, font:pygame.Font, ypadding = 0, xpadding = 0, aa = False):
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        y = ypadding
        lineSpacing = -2
        
        #Get Font Height:
        font_height = font.size("Tg")[1]

        while text:
            i = 1

            if y + font_height + ypadding > rect.height:
                break
            
            while font.size(text[:i+1])[0] < rect.width - 2*xpadding and i < len(text):
                i += 1

            if i < len(text):
                i = text.rfind(" ",0 , i) + 1

            image = font.render(text[:i], aa, color)
            surface.blit(image, (xpadding, y))
            y += font_height + lineSpacing

            text = text[i:]

        return surface, text

            


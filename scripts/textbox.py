from scripts.layeredsprite import LayeredSprite
import pygame

class TextBox(LayeredSprite):

    theme_defaults = {
        "background": "#00000000",
        "text_color": "#000000FF",
        "shape": "rect",
        "y_padding": 0,
        "x_padding": 0,
        "horizontal_alignment": "left",
        "vertical_alignment": "top",
        "scale_image": False,
        "glow": None,
        "glow_radius": 1
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
        self.horizontal_alignment = self.theme.get("horizontal_alignment", self.theme_defaults["horizontal_alignment"])
        self.vertical_alignment = self.theme.get("vertical_alignment", self.theme_defaults["vertical_alignment"])
        self.glow = self.theme.get("glow", self.theme_defaults["glow"])
        self.glow_radius = self.theme.get("glow_radius", self.theme_defaults["glow_radius"])
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
        self.normal_surface = None  #Triggers Rebuild

    def build_surfaces(self):
        super().build_surfaces()

        if self.text_renderer is not None:
            text_surface, unblited, text_rect = TextBox.drawText(self.text[:self.display_pos], self.text_color, self.rect, self.text_renderer, self.y_padding, self.x_padding, 
                                                                 self.antialias, self.horizontal_alignment, self.glow, self.glow_radius)

            if self.vertical_alignment == "top":
                self.normal_surface.blit(text_surface, (0,0))
            elif self.vertical_alignment == "bottom":
                self.normal_surface.blit(text_surface, (0, self.rect.height - text_rect.height))
            elif self.vertical_alignment == "center":
                self.normal_surface.blit(text_surface, (0, self.rect.height/2 - text_rect.height/2))
            else:
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


    def drawText(text:str, color, rect:pygame.Rect, font:pygame.Font, ypadding = 0, xpadding = 0, aa = False,
                 text_alignment:str = "left", glow = None, glow_radius:int = 1):
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        y = ypadding
        lineSpacing = -2
        text_rect = pygame.Rect()

        #Get Font Height:
        font_height = font.size("Tg")[1]

        line = 1
        while text:
            i = 1

            if y + font_height + ypadding > rect.height:
                break
            
            while font.size(text[:i+1])[0] < rect.width - 2*xpadding and i < len(text):
                i += 1

            if i < len(text):
                i = text.rfind(" ",0 , i) + 1


            image = font.render(text[:i], aa, color)
            
            if text_alignment == "left":
                location = (xpadding, y)
            elif text_alignment == "right":
                location = (rect.width-xpadding-image.get_width(), y)
            elif text_alignment == "center":
                location = (rect.width/2 - image.get_width()/2, y)
            else:
                location = (xpadding, y)
            
            surface.blit(image, location)
            if line == 1:
                text_rect.left = location[0]
                text_rect.top =  location[1]
                text_rect.width = image.get_width()
                text_rect.height = image.get_height()
            else:
                text_rect.left = location[0] if location[0] < text_rect.left else text_rect.left 
                text_rect.width = image.get_width() if image.get_width() > text_rect.width else text_rect.width
                text_rect.height += font_height + lineSpacing

            y += font_height + lineSpacing
            text = text[i:]

            line += 1

        return surface, text, text_rect

            


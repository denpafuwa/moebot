from ..core import *
import math

class Quad(GameObject):
    def __init__(self, x=0, y=0, width=1, height=1, rotation=0, color=WHITE, tag="GameObject"):
        super().__init__(x, y, width, height, tag)
        self.rotation = rotation
        self.color = color
        self.origin = Vector2(0, 0)
        self.visible = True
    
    def draw(self):
        if self.visible:
            draw_rectangle_pro(Rectangle(self.position.x, self.position.y, self.size.x, self.size.y), self.origin, self.rotation, self.color)

class Sprite(GameObject):
    def __init__(self, x, y, path, tag = "Sprite"):
        super().__init__(tag)
        self.texture = None
        self.load_graphic(path)
        self.position = Vector2(x, y)
        self.scale = 1
        self.rotation = 0
        self.color = WHITE
        self.visible = True
    
    def load_graphic(self, path):
        self.texture = load_texture(path)

    def update(self, delta):
        pass

    def draw(self):
        if self.visible:
            draw_texture_ex(self.texture, self.position, self.rotation, self.scale, self.color)
    
    def unload(self):
        unload_texture(self.texture)

class Text(GameObject):
    def __init__(self, x, y, text, font_path = "", font_size = 16, color = WHITE, tag="Text"):
        super().__init__(x, y, 1, 1, tag)
        self.text = text
        self.font = FontLoader.font(font_path)
        self.font_size = font_size
        self.spacing = 2
        self.color = color
        self.visible = True
        self.wavy = False
        self.time_offset = 0
        self.frequency = 0.4
        self.amplitude = 15
        self.wavy_line_spacing = 1.5
    
    def enable_wave_effect(self, frequency, amplitude):
        self.frequency = frequency
        self.amplitude = amplitude
        self.wavy = True
    
    def disable_wave_effect(self):
        self.wavy = False

    def update(self, delta):
        self.time_offset += delta
        self.size = self.get_measurements()

    def draw(self):
        if self.visible:
            if self.wavy:
                char_x = self.position.x
                char_y = self.position.y
                for i, char in enumerate(self.text):
                    if char == '\n':
                        char_y += self.font_size + self.wavy_line_spacing
                        char_x = self.position.x
                    wave_offset = math.sin(self.time_offset + i * self.frequency) * self.amplitude
                    draw_text_ex(self.font, char, Vector2(char_x, char_y + wave_offset), self.font_size, self.spacing, self.color)
                    measured = measure_text_ex(self.font, char, self.font_size, self.spacing)
                    char_x += measured.x + self.spacing
            else:
                draw_text_ex(self.font, self.text, self.position, self.font_size, self.spacing, self.color)

    def get_measurements(self):
        return measure_text_ex(self.font, self.text, self.font_size, self.spacing)

class TypewriterText(Text):
    def __init__(self, x = 0, y = 0, text = "", delay = 1/24, font_path="", font_size=16, color=WHITE, tag="Text"):
        super().__init__(x, y, "", font_path, font_size, color, tag)
        self.prefix = ""
        self.set_text(text)
        self.delay = 1/24
        self.timer = 0.0
        self.typing = False
        self.done = False
        self.carat = 0

    def set_text(self, text):
        self.final_text = text
    
    def type(self):
        self.carat = 0
        self.timer = 0
        self.text = self.prefix + self.final_text[0:self.carat]
        self.done = False
        self.typing = True

    def update(self, delta):
        super().update(delta)
        if self.typing:
            self.timer += delta
            if self.timer >= self.delay:
                self.carat += 1
                self.text = self.prefix + self.final_text[0:self.carat]
                self.timer = 0
        self.done = self.text == self.prefix + self.final_text
        self.typing = not (self.carat == len(self.final_text))
    
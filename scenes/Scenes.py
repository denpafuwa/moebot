from engine.core import Scene, Mouse, FontLoader, SoundObject, Game
from engine.graphics import Text, TypewriterText, Quad
from pyray import *

class InitScene(Scene):
    def init(self):
        FontLoader.font("assets/ark-pixel.ttf")
        text = Text(20, 20, "This is the initial scene!\nWelcome to the NHK!")
        text.enable_wave_effect(.1, 5)
        text.spacing = 2
        text2 = TypewriterText(20, 60, "Hello, world! This is the typewriter text.\nLorem ipsum\nRandom text here\nNHK ni Youkoso", font_path="assets/ark-pixel.ttf", tag="lol")
        text2.enable_wave_effect(.3, 3)
        text2.spacing = 0
        text2.prefix = "OUTPUT: "
        self.add(text)
        self.add(text2)
        quad = Quad(0, 0, get_screen_width(), get_screen_height(), 0, Color(25, 177, 98, 255//2))
        self.add(quad)
        Game.load_music("assets/Morning.mp3")
        Game.play_music()
    
    def update(self, delta):
        text2: TypewriterText = self.get("lol")
        if is_key_pressed(KeyboardKey.KEY_ENTER) and (text2.done or not text2.typing):
            text = self.get("Text")
            text.text = "Enter pressed!"
            text2.set_text("Congrats on pressing enter! - ENTER押しておめでとう!")
            text2.type()

        
        super().update(delta)
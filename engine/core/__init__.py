from pyray import *

class Game:
    cur_scene = None
    cur_music = None

    def switch_scene(scene: Scene):
        if Game.cur_scene is not None:
            scene.unload()
        Game.cur_scene = scene
        scene.init()

    def load_music(path):
        if Game.cur_music is not None:
            Game.unload_music()
        Game.cur_music = load_music_stream(path)

    def play_music():
        play_music_stream(Game.cur_music)

    def resume_music():
        resume_music_stream(Game.cur_music)

    def pause_music():
        pause_music_stream(Game.cur_music)
    
    def update_music():
        if Game.cur_music is not None:
            update_music_stream(Game.cur_music)

    def unload_music():
        unload_music_stream(Game.cur_music)

class Mouse:
    def overlaps(obj: GameObject):
        return check_collision_point_rec(get_screen_to_world_2d(get_mouse_position(), Game.cur_scene.camera), Rectangle(obj.position.x, obj.position.y, obj.size.x, obj.size.y))

    def is_pressed():
        return is_mouse_button_pressed(0)
    
    def is_down():
        return is_mouse_button_down(0)

    def is_right_pressed():
        return is_mouse_button_pressed(1)
    
    def is_right_down():
        return is_mouse_button_down(1)

class Scene:
    def __init__(self):
        self.game_objects = list[GameObject]()
        self.camera = Camera2D(Vector2(0 ,0), Vector2(0, 0), 0, 1)
        pass

    def init(self):
        pass

    def update(self, delta):
        for go in self.game_objects:
            go.update(delta)

    def get(self, tag):
        for go in self.game_objects:
            if go.tag == tag:
                return go
        return None

    def add(self, game_object):
        self.game_objects.append(game_object)
    
    def remove(self, game_object):
        self.game_objects.remove(game_object)

    def draw(self):
        for go in self.game_objects:
            go.draw()
    
    def unload(self):
        for go in self.game_objects:
            go.unload()

class GameObject:
    def __init__(self, x = 0, y = 0, width = 1, height = 1, tag = "GameObject"):
        self.position = Vector2(x, y)
        self.size = Vector2(width, height)
        self.tag = tag
        self.visible = True
    
    def update(self, delta):
        pass

    def draw(self):
        pass

    def unload(self):
        pass

class SoundObject(GameObject):
    
    def __init__(self, path, tag="Sound"):
        super().__init__(0, 0, 1, 1, tag)
        self.sound_object = load_sound(path)
    
    def play(self):
        play_sound(self.sound_object)

    def resume(self):
        resume_sound(self.sound_object)

    def pause(self):
        pause_sound(self.sound_object)
    
    def update(self, delta):
        pass

    def draw(self):
        pass
    
    def unload(self):
        unload_sound(self.sound_object)

class FontLoader:

    fonts: dict[str, Font] = dict[str, Font]()

    def font(path):
        if not path or not path.strip():
            return get_font_default()
        if path in FontLoader.fonts.keys():
            return FontLoader.fonts[path]
        FontLoader.fonts[path] = load_font(path)
        return FontLoader.fonts[path]

    def font_jp(path, font_size = 92):
        if not path or not path.strip():
            return get_font_default()
        if path in FontLoader.fonts.keys():
            return FontLoader.fonts[path]
        codepoints = []
        codepoints.extend(range(0, 256))
        codepoints.extend(range(0x3040, 0x30A0))
        codepoints.extend(range(0x30A0, 0x3100))
        codepoints.extend(range(0x4E00, 0x9FB0))

        arr = ffi.new("int[%d]" % len(codepoints))

        for i, codepoint in enumerate(codepoints):
            arr[i] = codepoint

        ptr = ffi.cast("int *", arr)

        FontLoader.fonts[path] = load_font_ex(path, font_size, ptr, len(codepoints))
        return FontLoader.fonts[path]
        
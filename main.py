from pyray import *
from engine.core import *
from scenes import Scenes
from dialogue import *


init_window(800, 600, "Moe Robot!")

preloaded = False

Game.switch_scene(Scenes.InitScene())

content = ""
with open("assets/data/test.txt") as f:
    content = f.read()
    parsed = DialogueParser.parse(content)
    for p in parsed:
        print('EV:', p.event, '\nDATA:', p.data)

while not window_should_close():

    Game.cur_scene.update(get_frame_time())

    begin_drawing()
    begin_mode_2d(Game.cur_scene.camera)
    clear_background(BLACK)
    Game.cur_scene.draw()
    end_mode_2d()
    end_drawing()
Game.cur_scene.unload()
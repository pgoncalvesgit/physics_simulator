from typing import Dict

from .abstract_screen_manager import AbstractScreenManager
import pyglet as pg

DISPLAY = pg.canvas.Display()
SCREEN = DISPLAY.get_default_screen()
SCREEN_WIDTH = SCREEN.width
SCREEN_HEIGHT = SCREEN.height


class PygletScreenManager (AbstractScreenManager):

    def new_screen(self, width: int, height: int):
        print(width)
        print(height)
        new_window = pg.window.Window(resizable=True)
        new_window.set_size(width, height)
        new_window.set_location(int((SCREEN_WIDTH - width) / 2), int((SCREEN_HEIGHT - height) / 2))
        new_window.clear()
        self.screens[self.current_index] = new_window
        self.current_index += 1

    def close_screen(self, index: int):
        self.screens[index].close()

    def run(self):
        pg.app.run()

    def __init__(self):
        super().__init__()
        self.screens: Dict[int, pg.window.Window] = {}
        self.current_index = 0

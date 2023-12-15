import time
from typing import Dict

from .abstract_screen_manager import AbstractScreenManager
import os
import pygame as pg

pg.init()
CLOCK = pg.time.Clock()
DISPLAY = pg.display.Info()
SCREEN_WIDTH = DISPLAY.current_w
SCREEN_HEIGHT = DISPLAY.current_h


class PygameScreenManager(AbstractScreenManager):

    def new_screen(self, width: int, height: int):
        print(width)
        print(height)
        x = int((SCREEN_WIDTH - width) / 2)
        y = int((SCREEN_HEIGHT - height) / 2)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
        new_window = pg.display.set_mode((width, height))
        self.screens[self.current_index] = new_window
        self.current_index += 1

    def close_screen(self, index: int):
        pg.quit()

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            for i in self.screens.keys():
                self.screens[i].fill((255, 255, 255))
                pg.draw.circle(self.screens[i], (0, 0, 255), (250, 250), 75)
                pg.display.flip()
            CLOCK.tick(240)

    def __init__(self):
        super().__init__()
        pg.init()
        self.screens: Dict[int, pg.window.Window] = {}
        self.current_index = 0
        self.running = False

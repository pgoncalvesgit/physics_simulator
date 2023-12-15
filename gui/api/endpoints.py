from .abstract_screen_manager import AbstractScreenManager
from . import pyglet_screen_manager
from . import pygame_screen_manager

__screen_manager: AbstractScreenManager = pygame_screen_manager.PygameScreenManager()


def create_screen(width: int, height: int):
	__screen_manager.new_screen(width, height)


def run():
	__screen_manager.run()


def quit_screen(index: int):
	__screen_manager.close_screen(index)

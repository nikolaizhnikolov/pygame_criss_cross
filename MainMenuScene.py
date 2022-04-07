from Scene import Scene
import pygame
from pygame.surface import Surface


class MainMenuScene(Scene):
    def __init__(self):
        self.manager.set_static_level_objects(self.manager, {})
        self.manager.set_dynamic_level_objects(self.manager, {})

    def update(self):
        pass

    def render(self, surface: Surface):
        pass

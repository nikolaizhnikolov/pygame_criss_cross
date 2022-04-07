import builtins

from pygame.surface import Surface
from ObjectManager import ObjectManager


# Subclassed to provide Scenes with different functionality
# Uses a global ObjectManager
class Scene:

    manager = ObjectManager()

    def __init__(self):
        raise NotImplementedError

    def render(self, screen: Surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_input(self):
        raise NotImplementedError

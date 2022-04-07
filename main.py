import sys

import pygame
from pygame.locals import *
from Scene import Scene
from MainMenuScene import MainMenuScene
from ObjectManager import ObjectManager

# All errors are caught so this won't throw anything
# but each module can separately call .init() and return
# True or False success state
pygame.init()
# No need to call .quit() as it is automatically done by pygame

# First call to the manager. It uses a singleton pattern
# so this initializes the instance and gives us a reference to it.
# NB: Each Scene holds a reference to the instance.
manager = ObjectManager()

# Set screen size
screen = pygame.display.set_mode((400, 400))
screen.fill(color=(255, 255, 255))
width = screen.get_width()
height = screen.get_height()
# Load default font for writing out win/lose screen
font = pygame.font.SysFont(pygame.font.get_default_font(), size=64)

manager.add_shared_objects(manager, {'screen': screen,
                                     'width': width,
                                     'height': height,
                                     'font': font})

active_scene: Scene = MainMenuScene()

while True:
    events = pygame.event.get()

    # Handle shared inputs across levels
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    active_scene.handle_input(events)
    active_scene.update()
    active_scene.render(screen)


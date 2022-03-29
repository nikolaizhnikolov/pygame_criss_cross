# Import pygame
# * from pygame.locals imports a number of
# constants and functions to the global namespace
import sys

import pygame
from pygame.locals import *


class CellState:
    EMPTY = 0
    CIRCLE = 1
    CROSS = 2


# Dictionary of cell coordinates and states
cells = {(x // 3, x % 3): CellState.EMPTY for x in range(9)}
objects = {}


def load_image(path: str) -> pygame.surface:
    image = pygame.image.load(path).convert()
    if path.__contains__('png'):
        image.set_colorkey((0, 0, 255))
    return image


def scale_image(image: pygame.surface, width: int, height: int) -> pygame.surface:
    return pygame.transform.scale(image, (width, height))


def init() -> dict:
    # All errors are caught so this won't throw anything
    # but each module can separately call .init() and return
    # True or False success state
    pygame.init()
    # No need to call .quit() as it is automatically done by pygame
    # Set screen size
    screen = pygame.display.set_mode((400, 400))
    screen.fill(color=(255, 255, 255))
    # Set cell size (multiplied by window size)
    cell_width = screen.get_width() // 3
    cell_height = screen.get_height() // 3
    # Load images and scale
    circle = scale_image(load_image("assets/circle.png"), cell_width - 10, cell_height - 10)
    cross = scale_image(load_image("assets/cross.png"), cell_width - 10, cell_height - 10)
    # Load default font for writing out win/lose screen
    font = pygame.font.SysFont(pygame.font.get_default_font(), size=64)

    return {'screen': screen,
            'cell_width': cell_width,
            'cell_height': cell_height,
            'circle': circle,
            'cross': cross,
            'font': font}


objects = init()


def get_cell_image(cell: tuple) -> pygame.surface:
    state = cells[cell]
    if state == 1:
        return objects['circle']
    elif state == 2:
        return objects['cross']
    return None


def wins(cell: tuple) -> bool:
    x = cell[0]
    y = cell[1]

    col_values = [cells[a] for a in list(filter(lambda b: b[0] == x, cells))]
    row_values = [cells[a] for a in list(filter(lambda b: b[1] == y, cells))]

    return (row_values.count(row_values[0]) == 3) or \
           (col_values.count(col_values[0]) == 3)

    # if x % 2 == y % 2 == 0:
    #
    # elif x == y == 1:
    #     return 1 == cells[(0, 0)] == cells[(1, 1)] == cells[(2, 2)] or \
    #         1 == cells[(2, 0)] == cells[(1, 1)] == cells[(0, 2)] or \
    #         1 == cells[(1, 0)] == cells[(1, 1)] == cells[(1, 2)] or \
    #         1 == cells[(0, 1)] == cells[(1, 1)] == cells[(2, 1)]


def start_game():
    # Turn keeps track of whose turn is it to play
    # While it's true the next click will set a Circle, else a Cross
    turn = True

    screen: pygame.surface.Surface = objects.get('screen')
    width = screen.get_width()
    height = screen.get_height()
    cell_width = objects.get('cell_width')
    cell_height = objects.get('cell_height')
    font: pygame.font.Font = objects.get('font')

    loop = True
    # Game loop
    while loop:
        # Cycle all events in the queue
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                # Get mouse coordinates as a cell tuple
                mouse_position = pygame.mouse.get_pos()
                cell = (mouse_position[0] // cell_width, mouse_position[1] // cell_height)
                # Set to circle/cross depending on symbol and if state is inactive
                if cells[cell] == CellState.EMPTY:
                    cells[cell] = CellState.CIRCLE if turn else CellState.CROSS

                    if wins(cell):
                        winner: str = 'O' if turn else 'X'
                        win_text = font.render(winner + ' has won!', False, (255, 0, 0))
                        pygame.display.get_surface().blit(win_text, ((width - 64) // 2, (height - 64) // 2))

                    turn = not turn

                # TODO: Win Screen
                #  No lose screens will be in place
                #  The game will rotate which image to place and keep track with the dictionary
                #  On each turn it will calculate if any fields connected to the placed one form
                #  a winning row.

            # Press ESC to quit
            if event.type in (QUIT, K_q):
                print("ESCAPING FROM THIS HELL")
                loop = False

            # Redraw cells
            for cell in cells.keys():
                image = get_cell_image(cell)
                if image is not None:
                    screen.blit(image, (cell[0] * cell_width, cell[1] * cell_height))

            # Update screen
            pygame.display.update()
            pygame.time.delay(100)

    # On loop exit clean up and quit
    pygame.quit()
    sys.exit()


start_game()

import sys
import pygame
from pygame.locals import *
import CrissCrossUtil as util


class CellState:
    EMPTY = 0
    CIRCLE = 1
    CROSS = 2


# Dictionary of cell coordinates and states
cells = {(x // 3, x % 3): CellState.EMPTY for x in range(9)}
objects = {}


def win(cell: tuple) -> bool:
    x = cell[0]
    y = cell[1]

    col_values = [cells[a] for a in list(filter(lambda b: b[0] == x, cells))]
    row_values = [cells[a] for a in list(filter(lambda b: b[1] == y, cells))]
    row_win = row_values.count(row_values[0]) == 3
    col_win = col_values.count(col_values[0]) == 3
    # If row or col value is in a diagonal
    if x % 2 == 0 or y % 2 == 0:
        # Upper-left and down-right diagonal == values are equal to each other
        ldg_values = [cells[a] for a in list(filter(lambda b: b[0] == b[1], cells))]
        # Upper-right and down-left diagonal == values make a sum of 2
        # e.g. the amount of cols/rows for a given matrix
        # here it's 2 because we start from 0, so actually 3
        rdg_values = [cells[a] for a in list(filter(lambda b: b[0] + b[1] == 2, cells))]

        ldg_win = ldg_values[0] != 0 and ldg_values.count(ldg_values[0]) == 3
        rdg_win = rdg_values[0] != 0 and rdg_values.count(rdg_values[0]) == 3

        return row_win or col_win or ldg_win or rdg_win
    else:
        return row_win or col_win


def draw():
    return all(map(lambda d: cells[d] != 0, cells.keys()))


class GameScene(Scene):

    def __init__(self):
        # Set cell size (multiplied by window size)
        cell_width = self.manager.objects['shared']['screen'].get_width() // 3
        cell_height = screen.get_height() // 3
        # Load images and scale
        circle = util.scale_image(load_image("assets/circle.png"), cell_width - 10, cell_height - 10)
        cross = util.scale_image(load_image("assets/cross.png"), cell_width - 10, cell_height - 10)

        return {'screen': screen,
                'cell_width': cell_width,
                'cell_height': cell_height,
                'circle': circle,
                'cross': cross,
                'font': font}

    def render(self, screen: Surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError




objects = init()


def get_cell_image(cell: tuple) -> pygame.surface:
    state = cells[cell]
    if state == 1:
        return objects['circle']
    elif state == 2:
        return objects['cross']
    return None



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

                    # Win Screen
                    # No lose screens will be in place
                    # The game will rotate which image to place and keep track with the dictionary
                    # On each turn it will calculate if any fields connected to the placed one form
                    # a winning row.
                    if win(cell, cells):
                        winner: str = 'O' if turn else 'X'
                        win_text = font.render(winner + ' has won!', False, (255, 0, 0))
                        pygame.display.get_surface().blit(win_text, (
                            (width - win_text.get_width()) // 2, (height - win_text.get_height()) // 2))
                    elif draw(cells):
                        win_text = font.render('Draw!', False, (255, 0, 0))
                        pygame.display.get_surface().blit(win_text, (
                            (width - win_text.get_width()) // 2, (height - win_text.get_height()) // 2))
                    else:
                        turn = not turn

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

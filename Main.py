# TODO:
#  user inputs are different color before solve, then change to black for locked, and all solve() are grey

import pygame
import numpy as np
from functools import lru_cache

pygame.init()
pygame.font.init()

WIN_PIXELS, Y_SPACE = 720, 120
WIN = pygame.display.set_mode((WIN_PIXELS, WIN_PIXELS + Y_SPACE))
pygame.display.set_caption("Sudoku")
ICON = pygame.image.load("Sudoku Icon.png")
TITLE = "MAIN"
pygame.display.set_icon(ICON)
WHITE, BLACK, BLUE, GREY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (205, 205, 205)
L_RED, D_RED, PALE_BLUE, D_GREY = (255, 200, 200), (255, 0, 0), (120, 150, 210), (85, 85, 85)
CELL_SIZE, BOX_SIZE = int(WIN_PIXELS / 9), int(WIN_PIXELS / 3)
cell_x, cell_y, player_x, player_y, FPS = 0, 0, 0, 0, 60
is_locked = False
FPS_FONT = pygame.font.SysFont('arial', 15)
clock = pygame.time.Clock()
validity = np.ones((9, 9, 9), dtype=bool)
board = np.zeros((9, 9), dtype=int)
invalids = np.zeros((9, 9), dtype=bool)
locked_cells = np.zeros((9, 9), dtype=bool)


def validity_do(coordinates: tuple, num: int) -> None:
    if num:
        x, y = coordinates
        if not validity[(num - 1,) + coordinates]:
            invalids[coordinates] = True
        validity[num - 1, x, :] = False
        validity[num - 1, :, y] = False
        validity[:, x, y] = False
        box_x, box_y = x // 3 * 3, y // 3 * 3
        validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False


def check(coordinates: tuple[int, int], value: int) -> bool:
    if value:
        x, y = coordinates
        box_x, box_y = x // 3 * 3, y // 3 * 3
        return any(board[x, :] == value) or any(board[:, y] == value) or np.any(
            board[box_x:box_x + 3, box_y:box_y + 3] == value)
    return False


def num_update(coordinates: tuple, num: int) -> None:
    board[coordinates] = num
    validity_do(coordinates, num)


def solve() -> None:
    update = True
    while update:
        update = False
        compressed = np.einsum("ijk -> jk", validity.astype(int))
        cell_solve = np.where(compressed == 1)
        size = cell_solve[0].size
        if size:
            for i in range(size):
                x, y = cell_solve[0][i], cell_solve[1][i]
                num_update((x, y), np.where(validity[:, x, y] != 0)[0][0] + 1)
                update = True
        compressed = np.einsum("ijk -> ik", validity.astype(int))
        row_solve = np.where(compressed == 1)
        size = row_solve[0].size
        if size:  # columns
            for i in range(size):
                z, y = row_solve[0][i], row_solve[1][i]
                num_update((np.where(validity[z, :, y] != 0)[0][0], y), z + 1)
                update = True
        compressed = np.einsum("ijk -> ij", validity.astype(int))
        column_solve = np.where(compressed == 1)
        size = column_solve[0].size
        if size:
            for i in range(size):
                z, x = column_solve[0][i], column_solve[1][i]
                num_update((x, np.where(validity[z, x, :] != 0)[0][0]), z + 1)
                update = True
        # for x in range(3):
        #     for y in range(3):
        #         for z in range(9):
        #             if np.count_nonzero(validity[box_cells[x], box_cells[y], z]) == 1:
        #                 coords = np.where(validity[box_cells[x], box_cells[y], z] != 0)
        #                 num_update((coords[0][0], coords[0][1]), z + 1)


@lru_cache(maxsize=6)
def make_rect(x: int, y: int) -> object:
    return pygame.Rect((x * CELL_SIZE, y * CELL_SIZE + Y_SPACE), (CELL_SIZE, CELL_SIZE))


@lru_cache(maxsize=81)
def make_num(num_font: pygame.font, num: str, txt_color: tuple[int, int, int]):
    return num_font.render(num, True, txt_color)


def cell_draw() -> None:
    for x in range(9):
        for y in range(9):
            if board[x, y]:
                if board[x, y] == board[cell_x, cell_y]:
                    pygame.draw.rect(WIN, PALE_BLUE, make_rect(x, y))


def num_draw(num_font) -> None:
    for x in range(9):
        for y in range(9):
            if board[x, y]:
                if invalids[x, y]:
                    txt_color = D_RED

                elif locked_cells[x, y]:
                    txt_color = BLACK
                else:
                    txt_color = D_GREY
                WIN.blit(make_num(num_font, str(int(board[x, y])), txt_color),
                         (x * CELL_SIZE + 18, y * CELL_SIZE - 2 + Y_SPACE))



def board_draw() -> None:
    for x in range(0, WIN_PIXELS, CELL_SIZE):
        for y in range(Y_SPACE, WIN_PIXELS + Y_SPACE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(WIN, BLACK, rect, 1)
    for x in range(0, WIN_PIXELS, BOX_SIZE):
        for y in range(Y_SPACE, WIN_PIXELS + Y_SPACE, BOX_SIZE):
            rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(WIN, BLACK, rect, 3)
    fps_count = str(int(clock.get_fps()))
    fps_offset = FPS_FONT.size(fps_count)[0]
    text_surface = FPS_FONT.render(fps_count, True, (0, 0, 0))
    WIN.blit(text_surface, (WIN_PIXELS - fps_offset, 0))


def validity_draw() -> None:
    if np.any(invalids):
        invalid_list = np.where(invalids)
        invalid_list[:] = list(zip(invalid_list[0], invalid_list[1]))  # In place is better on mem but idk if its faster 
        if len(invalid_list):
            for coordinates in invalid_list:
                x, y = coordinates[0] * 80, coordinates[1] * 80 + Y_SPACE
                pygame.draw.rect(WIN, L_RED, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))


def movement(keys, local_x: int, local_y: int) -> tuple[int, int]:
    move = [True] * 4

    if keys[pygame.K_a] and keys[pygame.K_SPACE] and local_x > BOX_SIZE:
        local_x -= BOX_SIZE
    elif keys[pygame.K_a] and keys[pygame.K_SPACE] and local_x < BOX_SIZE:
        local_x = 0
    elif keys[pygame.K_a] and local_x > 0:
        local_x -= CELL_SIZE
    else:
        move[0] = False

    if keys[pygame.K_d] and keys[pygame.K_SPACE] and local_x < WIN_PIXELS - BOX_SIZE:
        local_x += BOX_SIZE
    elif keys[pygame.K_d] and keys[pygame.K_SPACE] and local_x > WIN_PIXELS - BOX_SIZE:
        local_x = 640
    elif keys[pygame.K_d] and local_x < WIN_PIXELS - CELL_SIZE:
        local_x += CELL_SIZE
    else:
        move[1] = False

    if keys[pygame.K_w] and keys[pygame.K_SPACE] and local_y > BOX_SIZE + Y_SPACE:
        local_y -= BOX_SIZE
    elif keys[pygame.K_w] and keys[pygame.K_SPACE] and local_y <= BOX_SIZE + Y_SPACE:
        local_y = Y_SPACE
    elif keys[pygame.K_w] and local_y > Y_SPACE:
        local_y -= CELL_SIZE
    else:
        move[2] = False

    if keys[pygame.K_s] and keys[pygame.K_SPACE] and local_y < WIN_PIXELS - BOX_SIZE:
        local_y += BOX_SIZE
    elif keys[pygame.K_s] and keys[pygame.K_SPACE] and local_y > WIN_PIXELS - BOX_SIZE:
        local_y = 640 + Y_SPACE
    elif keys[pygame.K_s] and local_y < WIN_PIXELS + Y_SPACE - CELL_SIZE:
        local_y += CELL_SIZE
    else:
        move[3] = False

    if any(move):
        clock.tick(10)

    return local_x, local_y


def main():
    global cell_x, cell_y, player_x, player_y, invalids, locked_cells, is_locked, clock
    player_x, player_y = 0, Y_SPACE
    font = pygame.font.SysFont('arial', CELL_SIZE)
    title_width = font.size(TITLE)[0]
    title_y_offset = (WIN_PIXELS - title_width) / 2
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        cell_x, cell_y = (int(player_x / CELL_SIZE), int((player_y - Y_SPACE) / CELL_SIZE))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.TEXTINPUT:
                if event.text in "0123456789" and not locked_cells[cell_x, cell_y]:
                    invalids[cell_x, cell_y] = check((cell_x, cell_y), int(event.text))
                    board[cell_x, cell_y] = int(event.text)
                elif event.text == "n":
                    invalids.fill(False), locked_cells.fill(False), board.fill(0), validity.fill(True)
                    is_locked = False
                elif event.text == "t":
                    validity.fill(True)
                    for x in range(9):
                        for y in range(9):
                            validity_do((x, y), board[x][y])
                    is_locked = not is_locked
                    if is_locked:
                        locked_cells = (board != 0)
                    solve()
                elif event.text == "z":
                    game = [[0, 3, 1, 6, 7, 0, 0, 0, 0],
                            [7, 9, 0, 0, 0, 0, 0, 3, 0],
                            [0, 0, 0, 0, 1, 3, 5, 7, 0],
                            [0, 8, 0, 5, 3, 0, 9, 0, 0],
                            [0, 0, 0, 0, 6, 0, 0, 8, 0],
                            [3, 0, 7, 8, 0, 2, 0, 4, 0],
                            [1, 5, 3, 4, 8, 9, 0, 0, 0],
                            [0, 0, 8, 0, 0, 0, 0, 0, 0],
                            [0, 0, 9, 0, 0, 0, 8, 0, 4]]
                    for x in range(9):
                        for y in range(9):
                            num_update((x, y), game[x][y])

        keypress = pygame.key.get_pressed()
        player_x, player_y = movement(keypress, player_x, player_y)

        WIN.fill(GREY)
        validity_draw()
        cell_draw()
        pygame.draw.rect(WIN, BLUE, pygame.Rect(player_x, player_y, CELL_SIZE - 1, CELL_SIZE - 1))
        board_draw()
        title_surface = font.render(TITLE, True, BLACK)
        WIN.blit(title_surface, (title_y_offset, 5))
        num_draw(font)
        pygame.display.update()

        if keypress[pygame.K_q]:
            clock.tick(20)
            print(f"----------\nCell: ({cell_x}, {cell_y})\nValidity set: {validity[:, cell_x, cell_y]}\n----------")
        elif keypress[pygame.K_e]:
            print(np.swapaxes(validity, 2, 1))
    pygame.quit()


main()

'''
Easy:
[[4, 0, 9, 0, 7, 2, 0, 1, 3],
 [7, 0, 2, 8, 3, 0, 6, 0, 0],
 [0, 1, 6, 0, 4, 9, 8, 7, 0],
 [2, 0, 0, 1, 0, 0, 0, 6, 0],
 [5, 4, 7, 0, 0, 0, 2, 0, 0],
 [6, 9, 0, 0, 0, 4, 0, 3, 5],
 [8, 0, 3, 4, 0, 0, 0, 0, 6],
 [0, 0, 0, 0, 0, 3, 1, 0, 0],
 [0, 6, 0, 9, 0, 0, 0, 4, 0]]

Medium:
[[0, 3, 1, 6, 7, 0, 0, 0, 0],
 [7, 9, 0, 0, 0, 0, 0, 3, 0],
 [0, 0, 0, 0, 1, 3, 5, 7, 0],
 [0, 8, 0, 5, 3, 0, 9, 0, 0],
 [0, 0, 0, 0, 6, 0, 0, 8, 0],
 [3, 0, 7, 8, 0, 2, 0, 4, 0],
 [1, 5, 3, 4, 8, 9, 0, 0, 0],
 [0, 0, 8, 0, 0, 0, 0, 0, 0],
 [0, 0, 9, 0, 0, 0, 8, 0, 4]]'''

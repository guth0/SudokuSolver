# TODO:
#  The bastard is validlity remove

import pygame
import time
import numpy as np
import numpy.ma as ma

pygame.init()
pygame.font.init()

WIN_PIXELS, Y_SPACE = 720, 120
WIN = pygame.display.set_mode((WIN_PIXELS, WIN_PIXELS + Y_SPACE))
pygame.display.set_caption("Sudoku")
ICON = pygame.image.load('Sudoku Icon.png')
TITLE = "Format Testing"
pygame.display.set_icon(ICON)
WHITE, BLACK, BLUE, GREY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (205, 205, 205)
L_RED, D_RED, PALE_BLUE, D_GREY = (255, 200, 200), (255, 0, 0), (120, 150, 210), (85, 85, 85)
CELL_SIZE, BOX_SIZE = int(WIN_PIXELS / 9), int(WIN_PIXELS / 3)
cell_x, cell_y, player_x, player_y, FPS = 0, 0, 0, 0, 60
is_locked = False
FPS_FONT = pygame.font.SysFont('arial', 15)
clock = pygame.time.Clock()
validity = np.full((9, 9, 9), True)
board = np.zeros((9, 9), dtype=int)
invalids = np.full((9, 9), False)
locked_cells = np.full((9, 9), False)


def validity_undo(coordinates: tuple) -> None:  # Bastard code
    if board[coordinates]:
        temp_board = ma.masked_where(board != board[coordinates], board, True)
        x, y = coordinates
        for i in range(9):
            if not any(board[x, :] == i + 1) or not any(board[:, y] == i + 1):
                validity[i, x, y] = True
        validity[board[coordinates] - 1, x, y] = False
        for i in range(9):
            if all(temp_board.mask[:, i]) and not board[x, i]:
                validity[board[coordinates] - 1, x, i] = True
            if all(temp_board.mask[i, :]) and not board[x, i]:
                validity[board[coordinates] - 1, i, y] = True
        box_x, box_y = int(x / 3) * 3, int(y / 3) * 3
        if np.sum(temp_board.mask[box_x:box_x + 3, box_y:box_y + 3]) < 8:
            validity[board[coordinates] - 1, box_x:box_x + 3, box_y:box_y + 3] = False
        else:
            validity[board[coordinates] - 1, box_x:box_x + 3, box_y:box_y + 3] = True
        if invalids[coordinates]:
            invalids[coordinates] = False


def validity_do(coordinates: tuple, num: int) -> None:
    if num:
        x, y = coordinates
        if not validity[(num - 1,) + (coordinates)]:
            invalids[coordinates] = True
        validity[num - 1, x, :] = False
        validity[num - 1, :, y] = False
        validity[:, x, y] = False
        box_x, box_y = int(x / 3) * 3, int(y / 3) * 3
        validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False


def num_update(coordinates: tuple, num: int) -> None:
    validity_undo(coordinates)
    board[coordinates] = num
    validity_do(coordinates, num)


def solve() -> None:  # This is not working at fucking all
    update = True
    # while update:
    update = False
    compressed = np.count_nonzero(validity, axis=0)
    cell_solve = np.where(compressed == 1)  # all of these need to be changed
    size = cell_solve[0].size
    if size:
        for i in range(size):
            x, y = cell_solve[0][i], cell_solve[1][i]
            if not board[x, y]:  # Shouldnt have to do this :(
                num_update((x, y), np.where(validity[:, x, y] != 0)[0][0] + 1)
                update = True
    compressed = np.count_nonzero(validity, axis=1)
    row_solve = np.where(compressed == 1)
    size = row_solve[0].size
    if size:  # columns
        for i in range(size):
            z, y = row_solve[0][i], row_solve[1][i]
            num_update((np.where(validity[z, :, y] != 0)[0][0], y), z + 1)
            update = True
    compressed = np.count_nonzero(validity, axis=2)
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
        #             if np.count_nonzero(validity[box_cells[x], box_cells[y], z]) == 1:  # Try and make this into an array like the other ones just for consistency I think, might be faster too
        #                 coords = np.where(validity[box_cells[x], box_cells[y], z] != 0)
        #                 num_update((coords[0][0], coords[0][1]), z + 1)


def num_draw(num_font) -> None:
    for x in range(9):
        for y in range(9):
            if board[x, y]:
                if invalids[x, y]:
                    color = D_RED
                elif board[x, y] == board[cell_x, cell_y]:
                    color = PALE_BLUE
                elif locked_cells[x, y]:
                    color = BLACK
                else:
                    color = D_GREY
                text_surface = num_font.render(str(int(board[x, y])), True, color)
                WIN.blit(text_surface, (x * CELL_SIZE + 18, y * CELL_SIZE - 2 + Y_SPACE))


def draw_main() -> None:
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
        invalid_list = list(zip(invalid_list[0], invalid_list[1]))
        if len(invalid_list):
            for coordinates in invalid_list:
                x, y = coordinates[0] * 80, coordinates[1] * 80 + Y_SPACE
                pygame.draw.rect(WIN, L_RED, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))


def movement(keys, local_x: int, local_y: int) -> tuple[int]:
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
        time.sleep(.09)

    return (local_x, local_y)


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
                    num_update((cell_x, cell_y), int(event.text))
                elif event.text == "n":
                    invalids.fill(False), locked_cells.fill(False), board.fill(0), validity.fill(True)
                elif event.text == "c":
                    is_locked = not is_locked
                    if is_locked:
                        locked_cells = (board != 0)
                elif event.text == "t":
                    solve()

        keypress = pygame.key.get_pressed()
        player_x, player_y = movement(keypress, player_x, player_y)

        WIN.fill(GREY)
        validity_draw()
        pygame.draw.rect(WIN, BLUE, pygame.Rect(player_x, player_y, CELL_SIZE - 1, CELL_SIZE - 1))
        draw_main()
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
array([[4, 0, 9, 0, 7, 2, 0, 1, 3],
       [7, 0, 2, 8, 3, 0, 6, 0, 0],
       [0, 1, 6, 0, 4, 9, 8, 7, 0],
       [2, 0, 0, 1, 0, 0, 0, 6, 0],
       [5, 4, 7, 0, 0, 0, 2, 0, 0],
       [6, 9, 0, 0, 0, 4, 0, 3, 5],
       [8, 0, 3, 4, 0, 0, 0, 0, 6],
       [0, 0, 0, 0, 0, 3, 1, 0, 0],
       [0, 6, 0, 9, 0, 0, 0, 4, 0]])'''

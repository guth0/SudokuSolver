import pygame
import time

pygame.init()
pygame.font.init()

WIN_PIXELS, Y_SPACE = 720, 120
WIN = pygame.display.set_mode((WIN_PIXELS, WIN_PIXELS + Y_SPACE))
pygame.display.set_caption("Sudoku")
ICON = pygame.image.load('Sudoku Icon.png')
TITLE = "Feature Testing"
pygame.display.set_icon(ICON)
WHITE, BLACK, BLUE, GREY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (205, 205, 205)
L_RED, D_RED, PALE_BLUE, D_GREY = (255, 200, 200), (255, 0, 0), (120, 150, 210), (85, 85, 85)
CELL_SIZE, BOX_SIZE = int(WIN_PIXELS / 9), int(WIN_PIXELS / 3)
cell_num, box_num, player_x, player_y, FPS = 0, 0, 0, 0, 60
invalids, locked_cells, inputs = [], [], ("1", "2", "3", "4", "5", "6", "7", "8", "9")
is_locked = False
FPS_FONT = pygame.font.SysFont('arial', 15)
clock = pygame.time.Clock()
box_cells = [[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26],
             [27, 28, 29, 36, 37, 38, 45, 46, 47], [30, 31, 32, 39, 40, 41, 48, 49, 50],
             [33, 34, 35, 42, 43, 44, 51, 52, 53], [54, 55, 56, 63, 64, 65, 72, 73, 74],
             [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]
row_cells = []
column_cells = []
for count in range(9):
    row_cells.append(list(range(count * 9, (count + 1) * 9)))
    column_cells.append(list(range(0 + count, 72 + 1 + count, 9)))


class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.box = int((pos % 9) / 3) + int(pos / 27) * 3
        self.row = int(pos / 9)
        self.column = pos % 9
        self.num = 0
        self.validity = ""  # could turn this into a set then check every time a certain number is altered to remove
        self.color = D_GREY
        self.invalid = False
        self.duce_num_type = list  # 0 = Row duce, 1 = Column duce, 2 = Not lined up (useless rn)

    def num_update(self, num):
        validity_remove(self.pos)
        self.num = int(num)
        validity_add(self.pos, int(num))


cells = []
for location in range(81):
    cells.append(Cell(location))


def cell_cordiantes(position):
    return (position - (int(position / 9) * 9)) * 80, int(position / 9) * 80 + Y_SPACE


def coordinates_cell():
    return int((player_y - Y_SPACE) / 80 * 9 + player_x / 80)


def lock():
    for obj in cells:
        if obj.num:
            locked_cells.append(obj.pos)
            obj.color = BLACK


def validity_remove(cell):
    if cells[cell].num:
        num = str(cells[cell].num)
        remove_cells = set(row_cells[cells[cell].row] + column_cells[cells[cell].column] + box_cells[cells[cell].box])
        for i in remove_cells:
            cells[i].validity = cells[i].validity.replace(num, "", 1)
        if cell in invalids:
            invalids.remove(cell)
            cells[cell].invalid = False


def validity_add(cell, imput):
    if imput:
        imput = str(imput)
        add_cells = set(row_cells[cells[cell].row] + column_cells[cells[cell].column] + box_cells[cells[cell].box])
        for x in add_cells:
            if not x == cell:
                cells[x].validity += imput
        if cell not in invalids and imput in cells[cell].validity:
            invalids.append(cell)
            cells[cell].invalid = True


# def duce_create(cell_list: list[Cell], num: int):
#     column_set = {None}
#     row_set = {None}
#     duce_cells = [obj.pos for obj in cell_list]
#     for obj in cell_list:  # check if any of the cells are already duces here
#         row_set.add(obj.row)
#         column_set.add(obj.column)
#     if len(row_set) == 1:  # Declare as duce and do validity
#         for obj in cell_list:
#             obj.duce_num_type = [num, 0]
#         for cell in row_cells[cell_list[0].row]:
#             if cell not in duce_cells:
#                 cells[cell].validity += str(num)
#     elif len(column_set) == 1:
#         for obj in cell_list:
#             obj.duce_num_type = [num, 1]
#         for cell in column_cells[cell_list[0].row]:
#             if cell not in duce_cells:
#                 cells[cell].validity += str(num)
#     elif len(cell_list) == 2:
#         for obj in cell_list:
#             obj.duce_num_type = [num, 2]


def solve():
    update = True
    while update:
        update = False
        for obj in cells:  # Solves Cells with only one option
            if not obj.num:  # It can only change 0 values
                validity_set = {*obj.validity}
                if len(validity_set) == 8:
                    for x in inputs:
                        if x not in validity_set:
                            obj.num_update(x)
        for x in range(9):  # test speed of separating box and row or keeping them together
            row_validity = ""  # could go cell by cell instead of box by box...
            for r in row_cells[x]:
                if not cells[r].num:
                    for value in inputs:
                        if value not in cells[r].validity:
                            row_validity += value
            column_validity = ""
            for c in column_cells[x]:
                if not cells[c].num:
                    for value in inputs:
                        if value not in cells[c].validity:
                            column_validity += value
            box_validity = ""
            for cell in box_cells[x]:
                if not cells[cell].num:
                    for value in inputs:
                        if value not in cells[cell].validity:
                            box_validity += value
            for y in inputs:
                if row_validity.count(y) == 1:
                    for cell in row_cells[x]:
                        if not cells[cell].num and y not in cells[cell].validity:
                            cells[cell].num_update(y)
                            cells[cell].color = (0, 100, 0)
                            update = True
                if column_validity.count(y) == 1:
                    for cell in column_cells[x]:
                        if not cells[cell].num and y not in cells[cell].validity:
                            cells[cell].num_update(y)
                            cells[cell].color = (0, 150, 0)
                            update = True
                if box_validity.count(y) == 1:
                    for cell in box_cells[x]:
                        if not cells[cell].num and y not in cells[cell].validity:
                            cells[cell].num_update(y)
                            cells[cell].color = (0, 255, 0)
                            update = True
                # elif box_validity.count(y) == 2:
                #     duce_cells = []
                #     for cell in box_cells[x]:
                #         if not cells[cell].num and y not in cells[cell].validity:
                #             duce_cells.append(cells[cell])
                #     duce_create(duce_cells, y)


def draw_main():
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


def validity_draw():
    for invalid in invalids:
        x, y = cell_cordiantes(invalid)
        pygame.draw.rect(WIN, L_RED, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))


def main():
    global cell_num, player_x, player_y, invalids, locked_cells, is_locked, cells, clock
    player_x, player_y = 0, Y_SPACE
    font = pygame.font.SysFont('arial', CELL_SIZE)
    title_width = font.size(TITLE)[0]
    title_y_offset = (WIN_PIXELS - title_width) / 2
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        cell_num = coordinates_cell()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.TEXTINPUT:
                if event.text in "0123456789" and cell_num not in locked_cells:
                    cells[cell_num].num_update(event.text)
                if event.text == "n":
                    cells = []
                    for index in range(81):
                        cells.append(Cell(index))
                    invalids, locked_cells = [], []
                if event.text == "c":
                    if is_locked:
                        for i in locked_cells:
                            cells[i].color = D_GREY
                        locked_cells = []
                        is_locked = False
                    else:
                        lock()
                        is_locked = True
                if event.text == "t":
                    solve()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_SPACE] and player_x > BOX_SIZE:
            player_x -= BOX_SIZE
        elif keys[pygame.K_a] and keys[pygame.K_SPACE] and player_x < BOX_SIZE:
            player_x = 0
        elif keys[pygame.K_a] and player_x > 0:
            player_x -= CELL_SIZE

        if keys[pygame.K_d] and keys[pygame.K_SPACE] and player_x < WIN_PIXELS - BOX_SIZE:
            player_x += BOX_SIZE
        elif keys[pygame.K_d] and keys[pygame.K_SPACE] and player_x > WIN_PIXELS - BOX_SIZE:
            player_x = 640
        elif keys[pygame.K_d] and player_x < WIN_PIXELS - CELL_SIZE:
            player_x += CELL_SIZE

        if keys[pygame.K_w] and keys[pygame.K_SPACE] and player_y > BOX_SIZE + Y_SPACE:
            player_y -= BOX_SIZE
        elif keys[pygame.K_w] and keys[pygame.K_SPACE] and player_y <= BOX_SIZE + Y_SPACE:
            player_y = Y_SPACE
        elif keys[pygame.K_w] and player_y > Y_SPACE:
            player_y -= CELL_SIZE

        if keys[pygame.K_s] and keys[pygame.K_SPACE] and player_y < WIN_PIXELS - BOX_SIZE:
            player_y += BOX_SIZE
        elif keys[pygame.K_s] and keys[pygame.K_SPACE] and player_y > WIN_PIXELS - BOX_SIZE:
            player_y = 640 + Y_SPACE
        elif keys[pygame.K_s] and player_y < WIN_PIXELS + Y_SPACE - CELL_SIZE:
            player_y += CELL_SIZE

        WIN.fill(GREY)
        validity_draw()
        pygame.draw.rect(WIN, BLUE, pygame.Rect(player_x, player_y, CELL_SIZE - 1, CELL_SIZE - 1))
        draw_main()

        title_surface = font.render(TITLE, True, BLACK)
        WIN.blit(title_surface, (title_y_offset, 5))

        for obj in cells:
            if obj.num:
                if obj.invalid:
                    color = D_RED
                elif obj.num == cells[cell_num].num:
                    color = PALE_BLUE
                else:
                    color = obj.color
                text_surface = font.render(str(obj.num), True, color)
                x, y = cell_cordiantes(obj.pos)
                WIN.blit(text_surface, (x + 18, y - 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d]:
            time.sleep(.09)

        pygame.display.update()

        if keys[pygame.K_q]:  # debug only
            clock.tick(20)
            if cells[cell_num].validity:
                invalid_list = list({*cells[cell_num].validity})
                print(
                    f"----------\nCell: {cell_num}\nValidity set: {invalid_list}\nDuce: {cells[cell_num].duce_num_type}"
                    f"\n----------")
            else:
                print(
                    f"----------\nCell: {cell_num}\nValidity set: None\nDuce: {cells[cell_num].duce_num_type}"
                    f"\n----------")
        if keys[pygame.K_o]:
            listy = [4, 0, 3, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 9, 0, 7, 0, 0, 0, 0, 6, 8, 0, 7, 0, 0, 0, 5, 0, 0, 0, 7, 0,
                     9, 0, 0, 0, 0, 2, 9, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 5, 0, 0, 0, 0, 1, 2, 0, 4, 7, 9, 0, 3, 4,
                     0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 6, 0, 0, 8]
            for i, number in enumerate(listy):
                cells[i].num_update(number)
    pygame.quit()


main()

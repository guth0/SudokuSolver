import numpy as np


def validation(board):
    validity = np.ones((9, 9, 9), dtype=bool)
    for x in range(9):
        for y in range(9):
            num = board[x, y]
            if num:
                validity[num - 1, x, :] = False
                validity[num - 1, :, y] = False
                validity[:, x, y] = False
                box_x, box_y = x // 3 * 3, y // 3 * 3
                validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False
    return validity


def solve(board) -> None:


    def num_update(coordinates: tuple[int, int], num: int) -> None:
        board[coordinates] = num
        validity_update(num,coordinates)


    def validity_update(num, coordinates):
        x, y = coordinates
        validity[num - 1, x, :] = False
        validity[num - 1, :, y] = False
        validity[:, x, y] = False
        box_x, box_y = x // 3 * 3, y // 3 * 3
        validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False

    validity = validation(board)
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


def main():
    board = np.zeros((9, 9), dtype=int)

    print("Input board row by row, with zeros for for blank spaces\nExample -- 002004539")
    for y in range(9):
            board[y, :] = [*input(f"Enter row {y+1}: ")]
    solve(board)
    print(f"Solution is:\n{board}")


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
 [0, 0, 9, 0, 0, 0, 8, 0, 4]]
'''

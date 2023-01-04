import numpy as np
from Backtracking import backtrack


def validation(board: np.ndarray) -> np.ndarray:
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


def solve(board: np.ndarray) -> np.ndarray:

    def num_update(coordinates: tuple[int, int], num: int) -> None:
        board[coordinates] = num
        validity_update(num, coordinates)

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
        # need to add bos wise solving

    if np.any(board == 0):
        board = backtrack(board)

    return board

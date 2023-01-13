import numpy as np


class Solution():

    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.validity = np.zeros((9, 9, 9), dtype=bool)

    def __repr__(self):
        string = " -------------------\n"
        for row in self.board:
            string += "|"
            for num in row:
                string += " " + str(num)
            string += " |\n"
        string += " -------------------"
        return string

    def row_validation(self, row: str, row_num: int, pre_solve: bool = False):
        for i, num in enumerate([*row]):
            if num != 0:
                self.board[row_num, i] = num
        if pre_solve:
            self.solve(backtracking=False)

    def validity_update(self, num: int, coordinates: tuple[int, int]):
        x, y = coordinates
        self.validity[num - 1, x, :] = False
        self.validity[num - 1, :, y] = False
        self.validity[:, x, y] = False
        box_x, box_y = x // 3 * 3, y // 3 * 3
        self.validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False

    def create_validation(self):
        self.validity = np.zeros((9, 9, 9), dtype=bool)
        for x in range(9):
            for y in range(9):
                num = self.board[x, y]
                if num:
                    self.validity_update(num, (x, y))

    def num_update(self, coordinates: tuple[int, int], num: int):
        self.board[coordinates] = num
        self.validity_update(num, coordinates)

    def solve(self, backtracking: bool = True):

        self.create_validation()
        update = True
        while update:
            update = False
            # Only one valid number in cell
            compressed = np.einsum("ijk -> jk", self.validity.astype(int))
            cell_solve = np.where(compressed == 1)
            size = cell_solve[0].size
            if size:
                for i in range(size):
                    x, y = cell_solve[0][i], cell_solve[1][i]
                    self.num_update((x, y), np.where(
                        self.validity[:, x, y] != 0)[0][0] + 1)
                    update = True

            # Only one valid position in column
            compressed = np.einsum("ijk -> ik", self.validity.astype(int))
            row_solve = np.where(compressed == 1)
            size = row_solve[0].size
            if size:  # columns
                for i in range(size):
                    z, y = row_solve[0][i], row_solve[1][i]
                    self.num_update(
                        (np.where(self.validity[z, :, y] != 0)[0][0], y), z + 1)
                    update = True

            # Only one valid position in row
            compressed = np.einsum("ijk -> ij", self.validity.astype(int))
            column_solve = np.where(compressed == 1)
            size = column_solve[0].size
            if size:
                for i in range(size):
                    z, x = column_solve[0][i], column_solve[1][i]
                    self.num_update(
                        (x, np.where(self.validity[z, x, :] != 0)[0][0]), z + 1)
                    update = True

            '''BROKEN'''
            # Only one valid positon in a box
            # for i in range(9):
            #     for x in range(3):
            #         for y in range(3):
            #             x_slice, y_slice = slice(
            #                 x*3, (x+1)*3), slice(y*3, (y+1)*3)
            #             num = np.count_nonzero(
            #                 validity[i, x_slice, y_slice])
            #             if num == 1:
            #                 cell = np.where(validity[i, x_slice, y_slice])
            #                 self.num_update((cell[0][0], cell[1][0]), i + 1)
            if backtracking and np.any(self.board == 0):
                self.backtrack(self.board)

    def backtrack(self, board: np.ndarray):
        # Find the next empty cell
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    for n in range(1, 10):
                        if self.is_valid(board, i, j, n):
                            board[i, j] = n
                            if self.backtrack(board):
                                return True
                            board[i, j] = 0
                    return False
        return True

    def is_valid(self, board: np.ndarray, row: int, col: int, num: int) -> bool:

        if (board[row, :] == num).any():
            return False

        if (board[:, col] == num).any():
            return False

        box_row = row - (row % 3)
        box_col = col - (col % 3)
        if (board[box_row:box_row+3, box_col:box_col+3] == num).any():
            return False

        return True

import numpy as np
from Backtracking import backtrack


class Solution():

    def __init__(self, board: np.ndarray):
        self.board = board
        self.validity = self.validation()
        self.solution = self.solve()

    def __repr__(self):
        string = " -------------------\n"
        for row in self.solution:
            string += "|"
            for num in row:
                string += " " + str(num)
            string += " |\n"
        string += " -------------------"
        return string

    def validation(self) -> np.ndarray:
        validity = np.ones((9, 9, 9), dtype=bool)
        for x in range(9):
            for y in range(9):
                num = self.board[x, y]
                if num:
                    validity[num - 1, x, :] = False
                    validity[num - 1, :, y] = False
                    validity[:, x, y] = False
                    box_x, box_y = x // 3 * 3, y // 3 * 3
                    validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False
        return validity

    def solve(self) -> np.ndarray:

        def num_update(coordinates: tuple[int, int], num: int) -> None:
            self.board[coordinates] = num
            validity_update(num, coordinates)

        def validity_update(num, coordinates):
            x, y = coordinates
            self.validity[num - 1, x, :] = False
            self.validity[num - 1, :, y] = False
            self.validity[:, x, y] = False
            box_x, box_y = x // 3 * 3, y // 3 * 3
            self.validity[num - 1, box_x:box_x + 3, box_y:box_y + 3] = False

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
                    num_update((x, y), np.where(
                        self.validity[:, x, y] != 0)[0][0] + 1)
                    update = True

            # Only one valid position in column
            compressed = np.einsum("ijk -> ik", self.validity.astype(int))
            row_solve = np.where(compressed == 1)
            size = row_solve[0].size
            if size:  # columns
                for i in range(size):
                    z, y = row_solve[0][i], row_solve[1][i]
                    num_update(
                        (np.where(self.validity[z, :, y] != 0)[0][0], y), z + 1)
                    update = True

            # Only one valid position in row
            compressed = np.einsum("ijk -> ij", self.validity.astype(int))
            column_solve = np.where(compressed == 1)
            size = column_solve[0].size
            if size:
                for i in range(size):
                    z, x = column_solve[0][i], column_solve[1][i]
                    num_update(
                        (x, np.where(self.validity[z, x, :] != 0)[0][0]), z + 1)
                    update = True

            # Only one valid positon in a box
            for i in range(9):
                for x in range(3):
                    for y in range(3):
                        x_slice, y_slice = slice(
                            x*3, (x+1)*3), slice(y*3, (y+1)*3)
                        num = np.count_nonzero(
                            self.validity[i, x_slice, y_slice])
                        if num == 1:
                            cell = np.where(self.validity[i, x_slice, y_slice])
                            num_update((cell[0][0], cell[1][0]), i + 1)

        # After nothing else can be calculated without guesses, we guess
        if np.any(self.board == 0):
            board = backtrack(self.board)

        return board

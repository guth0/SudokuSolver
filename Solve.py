import numpy as np


class Solution():

    def __init__(self):
        # column, row
        self.board = np.zeros((9, 9), dtype=int)
        # number, column, row
        self.validity = np.ones((9, 9, 9), dtype=bool)
        # number, column, row
        # self.duces = np.zeros((9, 9, 9), dtype=bool)

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
        for i, num in enumerate(row):
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
        for x in range(9):
            for y in range(9):
                num = self.board[x, y]
                if num != 0:
                    self.validity_update(num, (x, y))

    def num_update(self, coordinates: tuple[int, int], num: int):
        self.board[coordinates] = num
        self.validity_update(num, coordinates)

    def solve(self, backtracking: bool = True):

        def update_true():
            root_update = True
            update = True
            do_duces = True

        compressed_cell = np.zeros((9, 9), dtype=int)
        compressed_row = np.zeros((9, 9), dtype=int)
        compressed_column = np.zeros((9, 9), dtype=int)
        self.create_validation()
        root_update, do_duces = True, True
        while root_update:
            root_update = False

            update = True
            while update:
                update = False

                # Only one valid number in cell
                compressed_cell = np.einsum(
                    "ijk -> jk", self.validity.astype(int))
                cell_solve = np.where(compressed_cell == 1)
                size = cell_solve[0].size
                if size:
                    for i in range(size):
                        x, y = cell_solve[0][i], cell_solve[1][i]
                        self.num_update((x, y), np.where(
                            self.validity[:, x, y] != 0)[0][0] + 1)
                        update_true()

                # Only one valid position in column
                # Each row is a level, each column is a row
                compressed_row = np.einsum(
                    "ijk -> ik", self.validity.astype(int))
                row_solve = np.where(compressed_row == 1)
                size = row_solve[0].size
                if size:  # columns
                    for i in range(size):
                        z, y = row_solve[0][i], row_solve[1][i]
                        self.num_update(
                            (np.where(self.validity[z, :, y] != 0)[0][0], y), z + 1)
                        update_true()

                # Only one valid position in row
                # Each row is a level, each column is a column
                compressed_column = np.einsum(
                    "ijk -> ij", self.validity.astype(int))
                column_solve = np.where(compressed_column == 1)
                size = column_solve[0].size
                if size:
                    for i in range(size):
                        z, x = column_solve[0][i], column_solve[1][i]
                        self.num_update(
                            (x, np.where(self.validity[z, x, :] != 0)[0][0]), z + 1)
                        update_true()

            update = True
            while update:
                update = False

                '''BROKEN'''
                # Only one valid positon in a box
                for i in range(9):
                    for x in range(3):
                        for y in range(3):
                            x_slice, y_slice = slice(
                                x*3, (x+1)*3), slice(y*3, (y+1)*3)
                            num = np.count_nonzero(
                                self.validity[i, x_slice, y_slice])
                            if num == 1:
                                cell = np.where(
                                    self.validity[i, x_slice, y_slice])
                                self.num_update(
                                    (cell[0][0], cell[1][0]), i + 1)
                                update_true()

            # Might need to make two versions of self.duces because a
            #   row duce and column duce can overlap in the compression

            # Need to make it where cells that are in self.duces are not counted
            # Compress the duces by row and then
            #   multiply it by compressed_row and compressed_column
            # Try to do np.any(all the rows in self.duces) then multiply
            # might get rid of do_duces

            # No loop because compressed_row is updated in the first loop only
            if do_duces and (np.any(compressed_row == 2) or np.any(compressed_column == 2)):
                do_duces = False
                row_duces = np.where(compressed_row == 2)
                size = row_duces[0].size
                if size:
                    for i in range(size):
                        z, y = row_duces[0][i], row_duces[1][i]
                        duce = np.where(self.validity[z, :, y] == True)
                        # Put onto duces array
                        # self.duces[z, duce[0][0], y] = True
                        # self.duces[z, duce[1][0], y] = True
                        # Add to validity
                        self.validity[z, :, y] = False
                        self.validity[z, duce[0][0], y] = True
                        self.validity[z, duce[0][1], y] = True
                        root_update = True

                column_duces = np.where(compressed_column == 2)
                size = column_duces[0].size
                if size:
                    for i in range(size):
                        z, x = column_duces[0][i], column_duces[1][i]
                        duce = np.where(self.validity[z, x, :] == True)
                        # Put onto duces array
                        # self.duces[z, x, duce[0][0]] = True
                        # self.duces[z, x, duce[1][0]] = True
                        # Add to validity
                        self.validity[z, x, :] = False
                        self.validity[z, x, duce[0][0]] = True
                        self.validity[z, x, duce[0][1]] = True
                        root_update = True

                # duces that are ontop of eachother are to be done here
                # look at compressed_row and compressed_column and
                #   see if there are 2 "2"'s in the same column
                # That means that there is two duces in the same row for different numbers
                # Then check if they are in the same cell
                # Think about if there are three duces in the same row/column

                # Could copy this work for "truces"??
                # Would need to do work/research to find
                #   combinations of duces and truces that lead to
                # three different cells that can only be those three numbers

            if backtracking and np.any(self.board == 0):
                self.backtrack(self.board)
                print("   --Backtracked--")

    def backtrack(self, board: np.ndarray) -> bool:
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

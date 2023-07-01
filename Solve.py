import numpy as np


def count_box_nonzeros(matrix: np.ndarray):
    reshaped_matrix = matrix.astype(int).reshape(3, 3, 3, 3)
    counts = np.einsum('ijkl->ik', reshaped_matrix)
    return counts


def is_valid_sudoku(grid):
    # Check rows
    for row in grid:
        if not is_valid_set(row):
            return False

    # Check columns
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not is_valid_set(column):
            return False

    # Check boxes
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = [grid[row][col]
                       for row in range(i, i + 3) for col in range(j, j + 3)]
            if not is_valid_set(subgrid):
                return False

    return True


def is_valid_set(nums):
    seen = set()
    for num in nums:
        if num != '.':
            if num in seen and num != 0:
                return False
            seen.add(num)
    return True


class Solution():

    def __init__(self):
        # column, row
        self.board = np.zeros((9, 9), dtype=int)
        # number, column, row
        self.validity = np.ones((9, 9, 9), dtype=bool)
        # number, column, row
        self.duces = np.ones((9, 9, 9), dtype=bool)
        self.count = 0

    def __repr__(self):
        string = " -------------------\n"
        for row in self.board:
            string += "|"
            for num in row:
                string += " " + str(num)
            string += " |\n"
        string += " -------------------\n"
        string += f"       {'VALID' if is_valid_sudoku(self.board) else 'INVALID'}"
        return string

    def row_impliment(self, row: str, row_num: int, pre_solve: bool = False):
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
        xbox, ybox = x // 3 * 3, y // 3 * 3
        self.validity[num - 1, xbox:xbox + 3, ybox:ybox + 3] = False

    def create_validation(self):
        for x in range(9):
            for y in range(9):
                num = self.board[x, y]
                if num != 0:
                    self.validity_update(num, (x, y))

    def num_update(self, coordinates: tuple[int, int], num: int):
        self.board[coordinates] = num
        self.validity_update(num, coordinates)
        # self.count += 1
        # print(f"Cell #{self.count} -- Solveable = {is_solvable(self)}")

    def solve(self, backtracking: bool = True):

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
                        self.num_update((x, y),
                                        np.where(self.validity[:, x, y] != 0)[0][0] + 1)
                        root_update, update, do_duces = True, True, True

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
                        root_update, update, do_duces = True, True, True

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
                        root_update, update, do_duces = True, True, True

            update = True
            while update:
                update = False
                for i in range(9):
                    compressed_box = count_box_nonzeros(self.validity[i])
                    box_solve = np.where(compressed_box == 1)
                    size = box_solve[0].size
                    if size:
                        for j in range(size):
                            x, y = box_solve[0][j], box_solve[1][j]
                            cell = np.where(
                                self.validity[i, x*3:(x+1)*3, y*3:(y+1)*3] == True)
                            self.num_update(
                                (cell[0][0] + x*3, cell[1][0] + y*3), i + 1)

                            root_update, update, do_duces = True, True, True

            # Might need to make two versions of self.duces because a
            #   row duce and column duce can overlap in the compression

            # Need to make it where cells that are in self.duces are not counted
            # Compress the duces by row and then
            #   multiply it by compressed_row and compressed_column
            # Try to do np.any(all the rows in self.duces) then multiply
            # might get rid of do_duces
            if do_duces:
                do_duces = False
                for z in range(9):
                    compressed_box = count_box_nonzeros(
                        self.validity[z] * self.duces[z])
                    duces_solve = np.where(compressed_box == 2)
                    size = duces_solve[0].size
                    if size:
                        for j in range(size):
                            x, y = duces_solve[0][j], duces_solve[1][j]
                            x_cells, y_cells = np.where(
                                self.validity[z, x*3:(x+1)*3, y*3:(y+1)*3] == True)

                            if np.all(x_cells):
                                self.validity[z, x_cells[0], :] = False

                            elif np.all(y_cells):
                                self.validity[z, :, y_cells[0]] = False

                            else:
                                continue
                            dx, dy = x*3, y*3

                            self.validity[z, x_cells[0] +
                                          dx, y_cells[0] + dy] = True
                            self.validity[z, x_cells[1] +
                                          dx, y_cells[1] + dy] = True

                            self.duces[z, x_cells[0] + dx,
                                       y_cells[0] + dy] = False
                            self.duces[z, x_cells[1] + dx,
                                       y_cells[1] + dy] = False

                            self.count += 1
                            print(f"Duce #{self.count} --> {z, x, y = }")
                            root_update, update = True, True

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
        if np.any(self.board == 0):
            if backtracking:
                self.backtrack(self.board)
                print("   --Backtracked--")
            else:
                print(" Currently Unsolvable")

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

        # Might need to be removed
        if (self.validity[num, row, col] == False):
            return False

        return True


# DEBUG TOOLS

# CHECK IF BOARD MATCHES WITH VALIDITY
def is_valid_validity(self):
    thing = np.ones((9, 9, 9), dtype=bool)
    for x in range(9):
        for y in range(9):
            num = self.board[x, y]
            if num != 0:
                thing[num - 1, x, :] = False
                thing[num - 1, :, y] = False
                thing[:, x, y] = False
                xbox, ybox = x // 3 * 3, y // 3 * 3
                thing[num - 1, xbox:xbox + 3, ybox:ybox + 3] = False

    return (np.array_equal(thing, self.validity))


# CHECK IF BOARD IS SOLVABLE
def is_solvable(self):
    array0 = self.board.copy()
    self.backtrack(array0)
    self.is_valid
    return (is_valid_sudoku(array0) and not np.any(array0 == 0))

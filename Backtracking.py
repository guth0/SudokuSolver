import numpy as np


def solve(board):
    # Find the next empty cell
    for i in range(9):
        for j in range(9):
            if (board[i] & (1 << board[i, j])).any():
                # Try each number from 1 to 9
                for n in range(1, 10):
                    # Check if the number is valid
                    if is_valid(board, i, j, n):
                        # Set the cell to the number and recursively try to solve the rest of the Sudoku
                        board[i, j] = n
                        if solve(board):
                            return True
                        # Reset the cell to zero and try the next number
                        board[i, j] = 0
                # If none of the numbers is valid, return false
                return False
    # If there are no more empty cells, the Sudoku is solved
    return True


def is_valid(board, row, col, num):
    # Check if the number is already in the row
    if (board[row] & (1 << num)).any():
        return False
    # Check if the number is already in the column
    if (board[:, col] & (1 << num)).any():
        return False
    # Check if the number is already in the 3x3 subgrid
    start_row = row - row % 3
    start_col = col - col % 3
    subgrid = board[start_row:start_row+3, start_col:start_col+3]
    if (subgrid & (1 << num)).any():
        return False
    # If the number is not in the row, column, or subgrid, it is valid
    return True


def backtrack(board):
    solve(board)
    return board

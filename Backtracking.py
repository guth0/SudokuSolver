import numpy as np


def solve(board):
    # Find the next empty cell
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                for n in range(1, 10):
                    if is_valid(board, i, j, n):
                        board[i, j] = n
                        if solve(board):
                            return True
                        board[i, j] = 0
                return False
    return True


def is_valid(board, row, col, num):
    if (board[row, :] == num).any():
        return False
    if (board[:, col] == num).any():
        return False
    box_row = row - row % 3
    box_col = col - col % 3
    if (board[box_row:box_row+3, box_col:box_col+3] == num).any():
        return False

    return True


def backtrack(board):
    solve(board)
    return board

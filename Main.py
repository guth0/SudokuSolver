# TODO:
#  Add "only one in box" to solve

import numpy as np
from Solve import solve


def main():
    board = np.zeros((9, 9), dtype=int)

    print("Input board row by row, with zeros for for blank spaces\nExample --- 002004539\n")
    for y in range(9):
        row = input(f"Enter row {y+1}: ").strip()
        while len(row) != 9 or not row.isdigit():
            print("Invalid input")
            row = input(f"Enter row {y+1}: ").strip()
        board[y, :] = [*row]

    box = ["003000000", "204000000", "509000000", "000000000",
           "000000000", "010000000", "000000000", "000000000", "000000000"]
    for i, level in enumerate(box):
        board[i, :] = [*level]
    print(f"Solution is:\n{solve(board)}")


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
Enter row 1: 003000000
Enter row 2: 204000000
Enter row 3: 509000000
Enter row 4: 000000000
Enter row 5: 000000000
Enter row 6: 000000000
Enter row 7: 000000000
Enter row 8: 000000000
Enter row 9: 010000000
box = ["003000000", "204000000", "509000000", "000000000", "000000000", "010000000", "000000000", "000000000", "000000000"]
    kat = ["031670000", "790000030", "000013570", "080530900",
           "000060080", "307802040", "153489000", "008000000", "009000804"]
'''

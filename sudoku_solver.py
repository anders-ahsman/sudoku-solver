#!/usr/bin/env python

from copy import deepcopy
from typing import Optional

from common import Board


def solve(board: Board) -> Optional[Board]:
    # only assigns valid numbers => if all positions are filled a solution has been found (base case)
    if all(board[row][col] != 0 for row in range(9) for col in range(9)):
        return board

    local_board: Board = deepcopy(board)
    for row in range(9):
        for col in range(9):
            if local_board[row][col] == 0:
                for n in range(1, 10):
                    if _is_possible(local_board, row, col, n):
                        local_board[row][col] = n
                        solution: Optional[Board] = solve(local_board)
                        if solution is not None:
                            return solution
                return None  # no solution for this branch, backtrack
    return None  # no solution possible


def _is_possible(board: Board, row: int, col: int, n: int) -> bool:
    if n in board[row]:
        return False

    for r in range(9):
        if board[r][col] == n:
            return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if board[r][c] == n:
                return False

    return True


if __name__ == '__main__':
    board_easy: Board = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    solution: Optional[Board] = solve(board_easy)
    if solution is None:
        print('No solution found!')
    else:
        for row in range(9):
            print(' '.join([str(n) for n in solution[row]]))

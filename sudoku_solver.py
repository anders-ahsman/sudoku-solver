#!/usr/bin/env python

from typing import List


board: List[List[int]] = [
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


def solve() -> None:
    global board

    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        board[y][x] = n
                        solve()
                        board[y][x] = 0  # reset position after backtracking
                return  # reached dead end, backtrack

    # arrived at solution
    for y in range(9):
        print(' '.join([str(n) for n in board[y]]))

    input('More?')  # can be more than one solution


def possible(x: int, y: int, n: int) -> bool:
    global board

    if n in board[y]:
        return False

    for i in range(9):
        if board[i][x] == n:
            return False

    y_start = (y // 3) * 3
    x_start = (x // 3) * 3
    for i in range(y_start, y_start + 3):
        for j in range(x_start, x_start + 3):
            if board[i][j] == n:
                return False

    return True


if __name__ == '__main__':
    solve()

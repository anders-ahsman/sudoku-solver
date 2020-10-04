from common import Board
from sudoku_board_extractor import extract_sudoku_board


def test_extract_sudoku_board__bathtub_image__returns_expected_board():
    # act
    board: Board = extract_sudoku_board('test_images/bathtub.jpg')

    # assert
    expected_board: Board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    assert board == expected_board


def test_extract_sudoku_board__bulls_image__returns_expected_board():
    # act
    board: Board = extract_sudoku_board('test_images/bulls.jpg')

    # assert
    expected_board: Board = [
        [0, 0, 0, 5, 0, 6, 0, 0, 0],
        [5, 6, 0, 0, 0, 3, 7, 2, 0],
        [0, 0, 2, 0, 7, 0, 4, 0, 0],
        [1, 0, 0, 7, 0, 0, 0, 0, 4],
        [0, 2, 3, 0, 6, 0, 0, 5, 1],
        [4, 0, 0, 0, 0, 5, 8, 0, 0],
        [0, 0, 9, 0, 5, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 1, 0],
        [2, 0, 0, 4, 0, 7, 3, 9, 0]
    ]
    assert board == expected_board

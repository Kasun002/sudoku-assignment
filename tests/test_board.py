import pytest
from sudoku.board import Board

# The classic example puzzle from the spec
SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

PREFILLED = {
    (0, 0), (0, 1), (0, 4),
    (1, 0), (1, 3), (1, 4), (1, 5),
    (2, 1), (2, 2), (2, 7),
    (3, 0), (3, 4), (3, 8),
    (4, 0), (4, 3), (4, 5), (4, 8),
    (5, 0), (5, 4), (5, 8),
    (6, 1), (6, 6), (6, 7),
    (7, 3), (7, 4), (7, 5), (7, 8),
    (8, 4), (8, 7), (8, 8),
}


@pytest.fixture
def board():
    return Board(SOLUTION, PREFILLED)


def test_prefilled_cells_are_set(board):
    assert board.grid[0][0] == 5
    assert board.grid[0][1] == 3
    assert board.grid[0][4] == 7


def test_non_prefilled_cells_are_empty(board):
    assert board.grid[0][2] == 0
    assert board.grid[0][3] == 0


def test_is_prefilled_returns_true_for_prefilled(board):
    assert board.is_prefilled(0, 0) is True
    assert board.is_prefilled(1, 5) is True


def test_is_prefilled_returns_false_for_empty(board):
    assert board.is_prefilled(0, 2) is False
    assert board.is_prefilled(8, 0) is False


def test_set_cell(board):
    board.set_cell(0, 2, 4)
    assert board.grid[0][2] == 4


def test_clear_cell(board):
    board.set_cell(0, 2, 4)
    board.clear_cell(0, 2)
    assert board.grid[0][2] == 0


def test_is_complete_returns_false_for_partial(board):
    assert board.is_complete() is False


def test_is_complete_returns_true_when_all_filled(board):
    for r in range(9):
        for c in range(9):
            board.grid[r][c] = SOLUTION[r][c]
    assert board.is_complete() is True


def test_get_empty_cells(board):
    empty = board.get_empty_cells()
    assert (0, 2) in empty
    assert (0, 0) not in empty  # prefilled
    assert len(empty) == 81 - len(PREFILLED)


def test_display_header(board):
    lines = board.display().split('\n')
    assert lines[0] == '    1 2 3 4 5 6 7 8 9'


def test_display_row_a(board):
    lines = board.display().split('\n')
    assert lines[1] == '  A 5 3 _ _ 7 _ _ _ _'


def test_display_row_i(board):
    lines = board.display().split('\n')
    assert lines[9] == '  I _ _ _ _ 8 _ _ 7 9'


def test_prefilled_count(board):
    assert len(PREFILLED) == 30

import pytest
from sudoku.validator import check


def make_empty_grid():
    return [[0] * 9 for _ in range(9)]


def test_no_violations_on_empty_grid():
    grid = make_empty_grid()
    assert check(grid) is None


def test_no_violations_on_valid_partial():
    grid = make_empty_grid()
    grid[0][0] = 5
    grid[0][1] = 3
    grid[0][4] = 7
    assert check(grid) is None


def test_row_violation():
    grid = make_empty_grid()
    grid[0][0] = 3
    grid[0][2] = 3  # duplicate 3 in row A
    result = check(grid)
    assert result == "Number 3 already exists in Row A."


def test_row_violation_row_b():
    grid = make_empty_grid()
    grid[1][0] = 6
    grid[1][5] = 6
    result = check(grid)
    assert result == "Number 6 already exists in Row B."


def test_column_violation():
    grid = make_empty_grid()
    grid[0][0] = 5
    grid[2][0] = 5  # duplicate 5 in column 1
    result = check(grid)
    assert result == "Number 5 already exists in Column 1."


def test_column_violation_col_9():
    grid = make_empty_grid()
    grid[0][8] = 2
    grid[5][8] = 2
    result = check(grid)
    assert result == "Number 2 already exists in Column 9."


def test_subgrid_violation():
    grid = make_empty_grid()
    # Place 8 in top-left 3x3 subgrid twice
    grid[0][0] = 8
    grid[1][2] = 8
    result = check(grid)
    assert result == "Number 8 already exists in the same 3\u00d73 subgrid."


def test_subgrid_violation_middle():
    grid = make_empty_grid()
    grid[3][3] = 7
    grid[4][5] = 7
    result = check(grid)
    assert result == "Number 7 already exists in the same 3\u00d73 subgrid."


def test_row_checked_before_column():
    grid = make_empty_grid()
    # Row A has duplicate 3, column 1 has duplicate 5
    grid[0][0] = 3
    grid[0][2] = 3
    grid[3][0] = 5
    grid[6][0] = 5
    result = check(grid)
    assert result is not None
    assert "Row A" in result


def test_valid_complete_board():
    grid = [
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
    assert check(grid) is None

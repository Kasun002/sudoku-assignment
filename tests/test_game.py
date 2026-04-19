import copy
import pytest
from sudoku.board import Board
from sudoku.game import Game

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
def game():
    board = Board(SOLUTION, PREFILLED)
    return Game(board)


@pytest.fixture
def full_game():
    """Game with every cell already filled (matches the solution)."""
    board = Board(SOLUTION, PREFILLED)
    board.grid = copy.deepcopy(SOLUTION)
    return Game(board)


def _parse_hint_cell(result: str) -> tuple[int, int]:
    """Return (row, col) indices from a hint string like 'Hint: Cell E5 = 5'."""
    cell = result.split()[2]
    return ord(cell[0]) - ord('A'), int(cell[1]) - 1


# --- Command parsing ---

def test_parse_place_command(game):
    assert game.parse_command("A3 4") == ('place', (0, 2, 4))


def test_parse_place_lowercase(game):
    assert game.parse_command("a3 4") == ('place', (0, 2, 4))


def test_parse_place_row_i(game):
    assert game.parse_command("I9 5") == ('place', (8, 8, 5))


def test_parse_clear_command(game):
    assert game.parse_command("C5 clear") == ('clear', (2, 4))


def test_parse_clear_lowercase(game):
    assert game.parse_command("c5 clear") == ('clear', (2, 4))


def test_parse_hint(game):
    assert game.parse_command("hint") == ('hint', None)


def test_parse_hint_uppercase(game):
    assert game.parse_command("HINT") == ('hint', None)


def test_parse_check(game):
    assert game.parse_command("check") == ('check', None)


def test_parse_quit(game):
    assert game.parse_command("quit") == ('quit', None)


def test_parse_empty_string(game):
    assert game.parse_command("") == ('invalid', None)


def test_parse_whitespace_only(game):
    assert game.parse_command("   ") == ('invalid', None)


def test_parse_invalid_row(game):
    assert game.parse_command("Z3 4") == ('invalid', None)


def test_parse_col_out_of_range(game):
    assert game.parse_command("A0 4") == ('invalid', None)
    assert game.parse_command("A10 4") == ('invalid', None)


def test_parse_number_out_of_range(game):
    assert game.parse_command("A3 0") == ('invalid', None)
    assert game.parse_command("A3 10") == ('invalid', None)


def test_parse_non_numeric_value(game):
    assert game.parse_command("A3 x") == ('invalid', None)


# --- Place handler ---

def test_handle_place_valid_move(game):
    success, msg = game.handle_place(0, 2, 4)
    assert success is True
    assert msg == "Move accepted."
    assert game.board.grid[0][2] == 4


def test_handle_place_prefilled_cell(game):
    success, msg = game.handle_place(0, 0, 6)
    assert success is False
    assert msg == "Invalid move. A1 is pre-filled."
    assert game.board.grid[0][0] == 5  # unchanged


# --- Clear handler ---

def test_handle_clear_valid(game):
    game.board.set_cell(0, 2, 4)
    success, msg = game.handle_clear(0, 2)
    assert success is True
    assert msg == "Move accepted."
    assert game.board.grid[0][2] == 0


def test_handle_clear_prefilled_cell(game):
    success, msg = game.handle_clear(0, 0)
    assert success is False
    assert msg == "Invalid move. A1 is pre-filled."


# --- Hint handler ---

def test_handle_hint_returns_correct_format(game):
    result = game.handle_hint()
    assert result.startswith("Hint: Cell ")
    assert "=" in result


def test_handle_hint_value_matches_solution(game):
    result = game.handle_hint()
    row, col = _parse_hint_cell(result)
    value = int(result.split()[4])
    assert SOLUTION[row][col] == value


@pytest.mark.parametrize("_", range(20))
def test_handle_hint_only_hints_empty_cells(game, _):
    result = game.handle_hint()
    row, col = _parse_hint_cell(result)
    assert game.board.grid[row][col] == 0


def test_handle_hint_no_empty_cells(full_game):
    assert full_game.handle_hint() == "No empty cells remaining."


# --- Check handler ---

def test_handle_check_valid_board(game):
    assert game.handle_check() == "No rule violations detected."


def test_handle_check_row_violation(game):
    game.board.set_cell(0, 2, 3)  # duplicate 3 in row A (A2 already has 3)
    result = game.handle_check()
    assert "Row A" in result


def test_handle_check_column_violation(game):
    game.board.set_cell(2, 0, 5)  # duplicate 5 in column 1 (A1 already has 5)
    result = game.handle_check()
    assert "Column 1" in result


def test_handle_check_subgrid_violation(game):
    # Place 9 at A3 — subgrid already has 9 at C2 (prefilled), no row/col conflict
    game.board.set_cell(0, 2, 9)
    result = game.handle_check()
    assert "subgrid" in result

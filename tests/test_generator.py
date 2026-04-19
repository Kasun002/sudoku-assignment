import itertools
import pytest
from sudoku.generator import generate_puzzle

COMPLETE_GROUP = list(range(1, 10))


@pytest.fixture(scope="module")
def solution():
    """Generate one valid solution, shared across all parametrized cases."""
    s, _ = generate_puzzle()
    return s


def _subgrid(solution, sr, sc):
    return [solution[r][c] for r in range(sr, sr + 3) for c in range(sc, sc + 3)]


# --- Solution validity ---

@pytest.mark.parametrize("r", range(9))
def test_solution_row_is_valid(solution, r):
    assert sorted(solution[r]) == COMPLETE_GROUP


@pytest.mark.parametrize("c", range(9))
def test_solution_col_is_valid(solution, c):
    col = [solution[r][c] for r in range(9)]
    assert sorted(col) == COMPLETE_GROUP


@pytest.mark.parametrize("sr,sc", list(itertools.product(range(0, 9, 3), range(0, 9, 3))))
def test_solution_subgrid_is_valid(solution, sr, sc):
    assert sorted(_subgrid(solution, sr, sc)) == COMPLETE_GROUP


# --- Prefilled positions ---

def test_generate_puzzle_has_30_prefilled_by_default():
    _, prefilled = generate_puzzle()
    assert len(prefilled) == 30


def test_generate_puzzle_custom_prefilled_count():
    _, prefilled = generate_puzzle(num_prefilled=25)
    assert len(prefilled) == 25


def test_generate_puzzle_prefilled_positions_within_bounds():
    _, prefilled = generate_puzzle()
    assert all(0 <= r <= 8 and 0 <= c <= 8 for r, c in prefilled)


def test_generate_puzzle_returns_different_puzzles():
    _, prefilled1 = generate_puzzle()
    _, prefilled2 = generate_puzzle()
    assert prefilled1 != prefilled2

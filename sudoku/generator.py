import itertools
import random


def _is_valid_placement(grid: list, row: int, col: int, num: int) -> bool:
    if num in grid[row]:
        return False
    if any(grid[r][col] == num for r in range(9)):
        return False
    sr, sc = (row // 3) * 3, (col // 3) * 3
    return all(
        grid[r][c] != num
        for r, c in itertools.product(range(sr, sr + 3), range(sc, sc + 3))
    )


def _fill(grid: list) -> bool:
    """Backtracking solver that fills the grid with a valid Sudoku solution."""
    for r, c in itertools.product(range(9), range(9)):
        if grid[r][c] == 0:
            nums = list(range(1, 10))
            random.shuffle(nums)
            for n in nums:
                if _is_valid_placement(grid, r, c, n):
                    grid[r][c] = n
                    if _fill(grid):
                        return True
                    grid[r][c] = 0
            return False
    return True


def generate_puzzle(num_prefilled: int = 30) -> tuple:
    """Return (solution, prefilled_positions) where solution is a complete valid board."""
    solution = [[0] * 9 for _ in range(9)]
    _fill(solution)

    all_positions = [(r, c) for r in range(9) for c in range(9)] # This
    random.shuffle(all_positions)
    prefilled = set(all_positions[:num_prefilled])

    return solution, prefilled

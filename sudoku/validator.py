import itertools

ROW_LABELS = 'ABCDEFGHI'


def _find_duplicate(nums: list) -> int | None:
    seen = set()
    for n in nums:
        if n in seen:
            return n
        seen.add(n)
    return None


def check(grid: list) -> str | None:
    """Check grid for rule violations. Returns the first violation message, or None."""
    for r in range(9):
        nums = [grid[r][c] for c in range(9) if grid[r][c] != 0]
        if dup := _find_duplicate(nums):
            return f"Number {dup} already exists in Row {ROW_LABELS[r]}."

    for c in range(9):
        nums = [grid[r][c] for r in range(9) if grid[r][c] != 0]
        if dup := _find_duplicate(nums):
            return f"Number {dup} already exists in Column {c + 1}."

    for sr, sc in itertools.product(range(0, 9, 3), range(0, 9, 3)):
        nums = [
            grid[r][c]
            for r in range(sr, sr + 3)
            for c in range(sc, sc + 3)
            if grid[r][c] != 0
        ]
        if dup := _find_duplicate(nums):
            return f"Number {dup} already exists in the same 3\u00d73 subgrid."

    return None

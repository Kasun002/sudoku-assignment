ROW_LABELS = 'ABCDEFGHI'


class Board:
    """Holds the puzzle state: the known solution, current player grid, and prefilled positions."""

    def __init__(self, solution: list, prefilled: set):
        self.solution = solution
        self.prefilled = prefilled
        self.grid = [[0] * 9 for _ in range(9)]
        for (r, c) in prefilled:
            self.grid[r][c] = solution[r][c]

    def is_prefilled(self, row: int, col: int) -> bool:
        return (row, col) in self.prefilled

    def set_cell(self, row: int, col: int, value: int):
        self.grid[row][col] = value

    def clear_cell(self, row: int, col: int):
        self.grid[row][col] = 0

    def is_complete(self) -> bool:
        return self.grid == self.solution

    def get_empty_cells(self) -> list:
        return [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]

    def display(self) -> str:
        lines = ['    1 2 3 4 5 6 7 8 9']
        for r in range(9):
            cells = ' '.join(str(self.grid[r][c]) if self.grid[r][c] != 0 else '_' for c in range(9))
            lines.append(f'  {ROW_LABELS[r]} {cells}')
        return '\n'.join(lines)

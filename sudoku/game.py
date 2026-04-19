import random
from sudoku.board import Board, ROW_LABELS
from sudoku.validator import check

VALID_ROWS = set(ROW_LABELS)


class Game:
    """Manages the game loop and user interaction."""

    def __init__(self, board: Board):
        self.board = board

    def parse_command(self, raw: str) -> tuple:
        """Parse a raw input string into (command_type, payload)."""
        parts = raw.strip().split()
        if not parts:
            return ('invalid', None)

        first = parts[0].upper()

        if first == 'HINT':
            return ('hint', None)
        if first == 'CHECK':
            return ('check', None)
        if first == 'QUIT':
            return ('quit', None)

        if len(parts) == 2:
            row_char = first[0]
            col_str = first[1:]

            if row_char not in VALID_ROWS:
                return ('invalid', None)
            try:
                col = int(col_str)
            except ValueError:
                return ('invalid', None)
            if col < 1 or col > 9:
                return ('invalid', None)

            row = ord(row_char) - ord('A')
            col -= 1

            action = parts[1].lower()
            if action == 'clear':
                return ('clear', (row, col))
            try:
                num = int(action)
                if 1 <= num <= 9:
                    return ('place', (row, col, num))
                return ('invalid', None)
            except ValueError:
                return ('invalid', None)

        return ('invalid', None)

    def handle_place(self, row: int, col: int, num: int) -> tuple:
        cell = f"{ROW_LABELS[row]}{col + 1}"
        if self.board.is_prefilled(row, col):
            return False, f"Invalid move. {cell} is pre-filled."
        self.board.set_cell(row, col, num)
        return True, "Move accepted."

    def handle_clear(self, row: int, col: int) -> tuple:
        cell = f"{ROW_LABELS[row]}{col + 1}"
        if self.board.is_prefilled(row, col):
            return False, f"Invalid move. {cell} is pre-filled."
        self.board.clear_cell(row, col)
        return True, "Move accepted."

    def handle_hint(self) -> str:
        empty = self.board.get_empty_cells()
        if not empty:
            return "No empty cells remaining."
        r, c = random.choice(empty)
        val = self.board.solution[r][c]
        return f"Hint: Cell {ROW_LABELS[r]}{c + 1} = {val}"

    def handle_check(self) -> str:
        error = check(self.board.grid)
        return error if error else "No rule violations detected."

    def run(self) -> bool:
        """Run the game loop. Returns True if the player wants to play again."""
        print("Welcome to Sudoku!\n")
        print("Here is your puzzle:")
        print(self.board.display())

        while True:
            print("\nEnter command (e.g., A3 4, C5 clear, hint, check, quit):")
            try:
                raw = input()
            except EOFError:
                break

            cmd_type, payload = self.parse_command(raw)

            if cmd_type == 'quit':
                print("Thanks for playing!")
                break

            elif cmd_type == 'hint':
                print(self.handle_hint())

            elif cmd_type == 'check':
                print(self.handle_check())

            elif cmd_type == 'place':
                row, col, num = payload
                success, msg = self.handle_place(row, col, num)
                print(f"\n{msg}\n\nCurrent grid:")
                print(self.board.display())
                if success and self.board.is_complete():
                    print("\nYou have successfully completed the Sudoku puzzle!")
                    print("Press any key to play again...")
                    input()
                    return True

            elif cmd_type == 'clear':
                row, col = payload
                _, msg = self.handle_clear(row, col)
                print(f"\n{msg}\n\nCurrent grid:")
                print(self.board.display())

            else:
                print("Invalid command. Please try again.")

        return False

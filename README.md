# Sudoku CLI

A command-line Sudoku game in Python.

## Requirements

- Python 3.10+
- pytest (for tests only)

## Setup

```bash
pip3 install -r requirements-dev.txt
```

## Run

```bash
python3 main.py
```

## Run Tests

```bash
python3 -m pytest tests/ -v
```

---

## How to Play

The board uses rows **A–I** and columns **1–9**.

| Command | Example | Description |
|---|---|---|
| Place a number | `A3 4` | Put 4 in row A, column 3 |
| Clear a cell | `C5 clear` | Remove your entry from C5 |
| Get a hint | `hint` | Reveals one correct cell |
| Check the board | `check` | Reports any rule violations |
| Quit | `quit` | Exit the game |

**Rules:**
- Pre-filled cells cannot be changed.
- Numbers must be 1–9.
- No duplicates in any row, column, or 3×3 box.
- Game ends when the board is completely and correctly filled.

from sudoku.generator import generate_puzzle
from sudoku.board import Board
from sudoku.game import Game


def main():
    while True:
        solution, prefilled = generate_puzzle()
        board = Board(solution, prefilled)
        game = Game(board)
        play_again = game.run()
        if not play_again:
            break


if __name__ == '__main__':
    main()

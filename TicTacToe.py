import Board
import AI
import UI

# TODO create loop for Tic Tac Toe game.

class TicTacToe:
    def __init__(self):
        self.board_class = Board.Board()

        self.board = self.board_class.board
        self.ai = AI.AI(self.board)
        self.ui = UI.UI(self.board)

    def start(self):
        self.ui.run()

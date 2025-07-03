import Board
import AI
import UI
import threading
import time


# TODO create loop for Tic Tac Toe game.

class TicTacToe:
    def __init__(self):
        self.board_class = Board.Board()

        self.board = self.board_class.board
        self.ai_mark = 'O'
        self.player_mark = 'X'
        self.ai = AI.AI(self.board_class, self.ai_mark, self.player_mark)
        self.ui = UI.UI(self.board_class, self.ai, self.ai_mark, self.player_mark)

        # self.remaining_move_list = []

        self.running = True

    def start(self):
        # start backend thread first (non-UI)
        # backend_thread = threading.Thread(target=self._backend)
        # backend_thread.start()

        # run pygame UI in main thread (blocking)
        self.ui.run()

        # when UI ends, stop backend loop and wait for it to finish
        self.running = False
        # self.board_class.__str__()
        # self.board_class.check_rows()
        # self.board_class.print_winner()

    # def _backend(self):

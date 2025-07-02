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
        self.ai = AI.AI(self.board, self.board_class)
        self.ui = UI.UI(self.board, self.board_class.size, self.board_class.field_number)
        self.running = True

    def start(self):
        # start backend thread first (non-UI)
        backend_thread = threading.Thread(target=self._backend)
        backend_thread.start()

        # run pygame UI in main thread (blocking)
        self.ui.run()

        # when UI ends, stop backend loop and wait for it to finish
        self.running = False
        backend_thread.join()

        # self.board_class.__str__()
        # self.board_class.check_rows()
        # self.board_class.print_winner()

    def _backend(self):
        while self.running:
            move_list = self.ui.get_player_moves()
            time.sleep(0.1)
            if len(move_list) > 0:
                move = move_list.pop()
                self._player_move(move)
                self.board_class.__str__()

    def _player_move(self, field):
        self._make_move('X', field)

    def _ai_move(self, field):
        self._make_move('O', field)

    def _make_move(self, player, field):
        if field is not None:
            self.board[field] = player

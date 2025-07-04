import Board
import AI
import UI
import threading
import time


class TicTacToe:
    def __init__(self):
        self.board_class = Board.Board()

        self.board = self.board_class.board
        self.ai_mark = 'O'
        self.player_mark = 'X'
        self.ai = AI.AI(self.board_class, self.ai_mark, self.player_mark)
        self.ui = UI.UI(self.board_class, self.ai, self.ai_mark, self.player_mark)

        self.turn = self.player_mark
        # self.remaining_move_list = []

        self.running = True

    def start(self):
        self.ui.run()
        # self.board_class.__str__()
        # while self.running and not self.board_class.is_full():
        #     if self.turn == self.player_mark:
        #         move = int(input(f"Your move ({self.player_mark}): "))
        #         if self.board_class.player_move(move):
        #             self.turn = self.ai_mark
        #         else:
        #             print("Invalid move, try again.")
        #     else:
        #         ai_move = self.ai.get_best_move()
        #         self.board_class.ai_move(ai_move)
        #         print(f"\nAI moves at {ai_move}")
        #         self.board_class.__str__()
        #         self.turn = self.player_mark
        #
        #     if self.board_class.check_for_win():
        #         print(f'\nWinner: {self.board_class.winner}')
        #         self.board_class.__str__()
        #         self.running = False
        #         break
        #
        # if self.board_class.is_full():
        #     print("Game ended in a draw.")



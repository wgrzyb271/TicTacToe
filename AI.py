import time
from math import inf


# TODO create AI with MIN-MAX Algorithm.

class AI:
    def __init__(self, board_class, ai_mark, player_mark):
        self.board_class = board_class
        self.ai_mark = ai_mark
        self.player_mark = player_mark
        self.best_move = 8

    def minimax(self, depth, is_maximizing_player, alpha=-inf, beta=inf) -> int:
        """
        Implementation of Minimax algorithm.
        alpha - maximizing score
        beta - minimizing score
        """
        self.board_class.check_for_win()
        if self.board_class.winner == self.player_mark:
            return 1
        elif self.board_class.winner == self.ai_mark:
            return -1
        elif self.board_class.is_full():
            return 0

        if is_maximizing_player:
            pass
            # self.pass_move()
            # self.board_class.ai_move(self.player_mark)
            # self.board_class.set_ai_move(0)
            # self.board_class.set_ai_move(8)
            # for move in self.board_class.available_moves():
            #     self.board_class.ai_move(move)
        else:
            # minimizing player
            pass


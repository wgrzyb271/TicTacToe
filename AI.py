import time
from math import inf


# TODO create AI with MIN-MAX Algorithm.
# TODO update best_move so the game won't stop.

class AI:
    def __init__(self, board_class, ai_mark, player_mark):
        self.board_class = board_class
        self.ai_mark = ai_mark
        self.player_mark = player_mark
        self.best_move = None
        self.legal_moves = [field for field in range(self.board_class.field_number)]
        self.moves_before = None

    def minimax(self, is_maximizing_player, depth=0, alpha=-inf, beta=inf) -> int:
        """
        Implementation of Minimax alpha beta pruning algorithm.
        alpha - maximizing score
        beta - minimizing score
        """
        self.board_class.check_for_win()
        if self.board_class.winner == self.player_mark:
            return -10
        elif self.board_class.winner == self.ai_mark:
            return 10
        elif self.board_class.is_full():
            return 0

        if is_maximizing_player:
            best_score = -inf
            for empty_field in self.board_class.available_moves():
                self.board_class.make_move(self.ai_mark, empty_field)
                vertex = self.minimax(depth=depth + 1, is_maximizing_player=False, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                best_score = max(vertex, best_score)
                if vertex >= beta:
                    return best_score
                elif vertex > alpha:
                    alpha = vertex
            return best_score
        else:
            best_score = inf
            for empty_field in self.board_class.available_moves():
                self.board_class.make_move(self.player_mark, empty_field)
                vertex = self.minimax(depth=depth + 1, is_maximizing_player=True, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                best_score = min(vertex, best_score)
                if vertex <= alpha:
                    return best_score
                elif vertex < beta:
                    beta = vertex
            return best_score

    def get_best_move(self):
        """Find the best move for AI using minimax"""
        best_score = -inf
        best_move = None

        # print(self.board_class.available_moves())

        for move in self.board_class.available_moves():
            # Make a calculating move
            self.board_class.board[move] = self.ai_mark
            # Recursively call minimax with the next depth and the minimizing player
            score = self.minimax(0, False)
            # Reset the move
            self.board_class.board[move] = "-1"

            # Update the best score
            if score > best_score:
                best_score = score
                best_move = move

        self.best_move = best_move
        return best_move

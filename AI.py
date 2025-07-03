import time
from math import inf


# TODO create AI with MIN-MAX Algorithm.
# TODO fix error with restoring legal moves - for now it restores only the last one move.

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
            return -1
        elif self.board_class.winner == self.ai_mark:
            return 1
        elif self.board_class.is_full():
            return 0

        legal_moves = self.board_class.available_moves()

        if is_maximizing_player:
            best_score = -inf
            for empty_field in legal_moves:
                self.board_class.make_move(self.ai_mark, empty_field)
                vertex = self.minimax(depth=depth + 1, is_maximizing_player=False, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                if vertex > best_score:
                    best_score = vertex
                elif vertex >= beta:
                    return best_score
                elif vertex > alpha:
                    alpha = vertex
            self.best_move = best_score
            return best_score
        else:
            best_score = inf
            for empty_field in legal_moves:
                self.board_class.make_move(self.player_mark, empty_field)
                vertex = self.minimax(depth=depth + 1, is_maximizing_player=True, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                if vertex < best_score:
                    best_score = vertex
                elif vertex <= alpha:
                    return best_score
                elif vertex < beta:
                    beta = vertex
            self.best_move = best_score
            return best_score

    def update_legal_moves(self, banned_move):
        if banned_move in self.legal_moves:
            self.legal_moves.remove(banned_move)

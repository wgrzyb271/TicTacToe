from math import inf



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
                self.board_class.ai_move(empty_field)
                score = self.minimax(depth=depth + 1, is_maximizing_player=False, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                best_score = max(score, best_score)
                if score >= beta:
                    return best_score
                elif score > alpha:
                    alpha = score
            return best_score
        else:
            best_score = inf
            for empty_field in self.board_class.available_moves():
                self.board_class.player_move(empty_field)
                score = self.minimax(depth=depth + 1, is_maximizing_player=True, alpha=alpha, beta=beta)
                self.board_class.undo_move(empty_field)

                best_score = min(score, best_score)
                if score <= alpha:
                    return best_score
                elif score < beta:
                    beta = score
            return best_score

    def get_best_move(self):
        """Find the best move for AI using minimax"""
        best_score = -inf
        best_move = None

        # print(self.board_class.available_moves())

        for move in self.board_class.available_moves():
            # Make a calculating move
            self.board_class.ai_move(move)
            # Recursively call minimax with the next depth and the minimizing player
            score = self.minimax(False, 0)
            # Reset the move
            self.board_class.undo_move(move)

            # Update the best score
            if score > best_score:
                best_score = score
                best_move = move

        self.best_move = best_move
        return best_move

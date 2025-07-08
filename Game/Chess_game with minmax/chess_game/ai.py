import math


class AIPlayer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def find_best_move(self, game_state):
        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in game_state.get_valid_moves():
            game_state.make_move(move)
            value = self.minimax(game_state, self.max_depth - 1, alpha, beta, False)
            game_state.undo_move()

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        return best_move

    def minimax(self, game_state, depth, alpha, beta, is_maximizing):
        if depth == 0 or game_state.is_checkmate() or game_state.is_stalemate():
            return self.evaluate_board(game_state)

        if is_maximizing:
            max_eval = -math.inf
            for move in game_state.get_valid_moves():
                game_state.make_move(move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, False)
                game_state.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game_state.get_valid_moves():
                game_state.make_move(move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, True)
                game_state.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, game_state):
        piece_values = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0,
            'P': -1, 'N': -3, 'B': -3, 'R': -5, 'Q': -9, 'K': 0
        }

        score = 0
        for row in game_state.board:
            for piece in row:
                if piece in piece_values:
                    score += piece_values[piece]
        return score
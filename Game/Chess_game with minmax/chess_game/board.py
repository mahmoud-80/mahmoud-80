from chess_game.move import Move


class Board:
    def __init__(self):
        self.board = self._create_start_board()
        self.white_to_move = True
        self.move_log = []

    def _create_start_board(self):
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '.'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        moves = self._generate_all_moves()
        return moves

    def _generate_all_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '.' and ((piece.isupper() and self.white_to_move) or
                                     (piece.islower() and not self.white_to_move)):
                    self._get_moves_for_piece(r, c, moves)
        return moves

    def _get_moves_for_piece(self, r, c, moves):
        piece = self.board[r][c].lower()
        if piece == 'p':
            self._get_pawn_moves(r, c, moves)
        elif piece == 'r':
            self._get_rook_moves(r, c, moves)
        elif piece == 'n':
            self._get_knight_moves(r, c, moves)
        elif piece == 'b':
            self._get_bishop_moves(r, c, moves)
        elif piece == 'q':
            self._get_queen_moves(r, c, moves)
        elif piece == 'k':
            self._get_king_moves(r, c, moves)

    def _get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            # حركة أمامية
            if self.board[r - 1][c] == '.':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '.':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # أكل
            for dc in [-1, 1]:
                if 0 <= c + dc < 8:
                    if self.board[r - 1][c + dc].islower():
                        moves.append(Move((r, c), (r - 1, c + dc), self.board))
        else:
            # نفس المنطق للأسود
            if self.board[r + 1][c] == '.':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '.':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            for dc in [-1, 1]:
                if 0 <= c + dc < 8:
                    if self.board[r + 1][c + dc].isupper():
                        moves.append(Move((r, c), (r + 1, c + dc), self.board))

    def _get_rook_moves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self._get_sliding_moves(r, c, moves, directions)

    def _get_knight_moves(self, r, c, moves):
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            if 0 <= r + dr < 8 and 0 <= c + dc < 8:
                target = self.board[r + dr][c + dc]
                if target == '.' or (self.white_to_move and target.islower()) or (
                        not self.white_to_move and target.isupper()):
                    moves.append(Move((r, c), (r + dr, c + dc), self.board))

    def _get_bishop_moves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self._get_sliding_moves(r, c, moves, directions)

    def _get_queen_moves(self, r, c, moves):
        self._get_rook_moves(r, c, moves)
        self._get_bishop_moves(r, c, moves)

    def _get_king_moves(self, r, c, moves):
        steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in steps:
            if 0 <= r + dr < 8 and 0 <= c + dc < 8:
                target = self.board[r + dr][c + dc]
                if target == '.' or (self.white_to_move and target.islower()) or (
                        not self.white_to_move and target.isupper()):
                    moves.append(Move((r, c), (r + dr, c + dc), self.board))

    def _get_sliding_moves(self, r, c, moves, directions):
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                target = self.board[nr][nc]
                if target == '.':
                    moves.append(Move((r, c), (nr, nc), self.board))
                elif (self.white_to_move and target.islower()) or (not self.white_to_move and target.isupper()):
                    moves.append(Move((r, c), (nr, nc), self.board))
                    break
                else:
                    break

    def is_checkmate(self):
        moves = self.get_valid_moves()
        return len(moves) == 0

    def is_stalemate(self):
        moves = self.get_valid_moves()
        return len(moves) == 0
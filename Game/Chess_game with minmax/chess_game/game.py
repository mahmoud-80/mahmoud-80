from chess_game.board import Board
from chess_game.move import Move
from chess_game.ai import AIPlayer


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.ai = AIPlayer()
        self.game_over = False

    def play(self):
        print("Welcome to Chess")
        print("Enter moves in algebraic notation ")

        while not self.game_over:
            self.print_board()

            if self.board.white_to_move:
                print("\nWhite's turn (Human)")
                move = self.get_human_move()
            else:
                print("\nBlack's turn (AI)")
                move = self.ai.find_best_move(self.board)
                print(f"AI plays: {move.get_chess_notation()}")

            self.board.make_move(move)

            if self.board.is_checkmate():
                winner = "White" if not self.board.white_to_move else "Black"
                print(f"Checkmate! {winner} wins!")
                self.game_over = True
            elif self.board.is_stalemate():
                print("Stalemate!")
                self.game_over = True

    def get_human_move(self):
        while True:
            try:
                move_str = input("Enter your move: ").strip().lower()
                if len(move_str) != 4:
                    raise ValueError("Move must be 4 characters (e.g., e2e4)")

                start_col = ord(move_str[0]) - ord('a')
                start_row = 8 - int(move_str[1])
                end_col = ord(move_str[2]) - ord('a')
                end_row = 8 - int(move_str[3])

                if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
                    raise ValueError("Invalid coordinates")

                move = Move((start_row, start_col), (end_row, end_col), self.board.board)

                valid_moves = self.board.get_valid_moves()
                if move in valid_moves:
                    return move
                else:
                    print("Invalid move. Try again.")
            except Exception as e:
                print(f"Error: {str(e)}. Please try again.")

    def print_board(self):
        print("\n   a b c d e f g h")
        print("  +-----------------+")
        for i, row in enumerate(self.board.board):
            print(f"{8 - i} | {' '.join(row)} | {8 - i}")
        print("  +-----------------+")
        print("   a b c d e f g h")
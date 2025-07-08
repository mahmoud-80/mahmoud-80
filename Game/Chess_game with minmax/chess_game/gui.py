import pygame
from chess_game.game import ChessGame


pygame.init()
WIDTH, HEIGHT = 600, 650
SQ_SIZE = 75
DIMENSION = 8
IMAGES = {}


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT = (247, 247, 105)


def load_images():

    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess AI ")
        self.clock = pygame.time.Clock()
        self.game = ChessGame()
        self.selected = None
        self.valid_moves = []
        self.font = pygame.font.SysFont('Arial', 20)
        load_images()

    def draw_board(self):

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = LIGHT_SQ if (row + col) % 2 == 0 else DARK_SQ
                pygame.draw.rect(self.screen, color,
                                 (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def draw_pieces(self):

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = self.game.board.board[row][col]
                if piece != '.':

                    if piece.islower():
                        key = 'b' + piece
                    else:
                        key = 'w' + piece.lower()

                    self.screen.blit(IMAGES[key], (col * SQ_SIZE, row * SQ_SIZE))

    def draw_highlight(self):

        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, HIGHLIGHT,
                             (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

    def draw_game_state(self):

        self.draw_board()
        self.draw_highlight()
        self.draw_pieces()
        self.draw_status()

    def draw_status(self):
        status_text = ""
        if self.game.board.is_checkmate():
            winner = "black" if self.game.board.white_to_move else "white"
            status_text = f"check! {winner} win!"
        elif self.game.board.is_stalemate():
            status_text = "drow!"
        else:
            status_text = "white turn" if self.game.board.white_to_move else "black turn"

        text_surface = self.font.render(status_text, True, BLACK)
        self.screen.blit(text_surface, (10, HEIGHT - 40))

    def handle_click(self, row, col):

        piece = self.game.board.board[row][col]


        if (piece != '.' and
                ((piece.isupper() and self.game.board.white_to_move) or
                 (piece.islower() and not self.game.board.white_to_move))):
            self.selected = (row, col)
            self.valid_moves = [move for move in self.game.board.get_valid_moves()
                                if move.start_row == row and move.start_col == col]
            return


        if self.selected:
            move = self.create_move(self.selected, (row, col))
            if move in self.valid_moves:
                self.game.board.make_move(move)
                self.selected = None
                self.valid_moves = []


                if not self.game.board.white_to_move and not self.game.board.is_checkmate():
                    ai_move = self.game.ai.find_best_move(self.game.board)
                    if ai_move:
                        self.game.board.make_move(ai_move)

    def create_move(self, start, end):

        from chess_game.move import Move
        return Move(start, end, self.game.board.board)

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        row, col = y // SQ_SIZE, x // SQ_SIZE
                        if row < 8 and col < 8:
                            self.handle_click(row, col)

            self.draw_game_state()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
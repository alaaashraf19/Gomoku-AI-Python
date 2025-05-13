import pygame as pg
from pygame.locals import *
from minimax import Gomoku

BOARD_SIZE = 15
CELL_SIZE = 40
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

LIGHT_BROWN = (222, 184, 135) 
DARK_BROWN = (160, 82, 45)  
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



class GomokuGui:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pg.display.set_caption("Gomoku")
        self.font = pg.font.Font(None, 36)
        self.clock = pg.time.Clock()
        self.game=Gomoku(BOARD_SIZE, "B", "W")
        self.current_player = "B"
        

    def draw_board(self, screen):
        board=self.game.board
        screen.fill(LIGHT_BROWN)  # Fill with light brown background
        
        # Draw grid lines in dark brown
        for i in range(BOARD_SIZE):
            # Horizontal lines
            pg.draw.line(screen, DARK_BROWN, 
                        (CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE),
                        (WINDOW_SIZE - CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE), 2)
            # Vertical lines
            pg.draw.line(screen, DARK_BROWN, 
                        (CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2),
                        (CELL_SIZE // 2 + i * CELL_SIZE, WINDOW_SIZE - CELL_SIZE // 2), 2)

        # Optional: draw small dots at star points to enhance board appearance (like real Go/Gomoku boards)
        star_points = [3, 7, 11]  # typical star points for 15x15
        for r in star_points:
            for c in star_points:
                center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                pg.draw.circle(screen, DARK_BROWN, center, 5)
        
        # Draw pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                if board[row][col] == "B":
                    pg.draw.circle(screen, BLACK, center, CELL_SIZE // 2 - 4)
                elif board[row][col] == "W":
                    pg.draw.circle(screen, WHITE, center, CELL_SIZE // 2 - 4)
                    pg.draw.circle(screen, BLACK, center, CELL_SIZE // 2 - 4, 1)  # Outline for white stones
                # Remove drawing for empty positions to show just board color and grid

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game.game_over():  # Left mouse button
                        x, y = event.pos
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE
                        if self.game.is_on_board(row, col):
                            if self.game.board[row][col] == " " and self.current_player == "B":
                                if self.game.make_move(row, col, self.current_player):
                                    if self.game.is_win(self.current_player):
                                        print(f"{self.current_player} wins!")
                                        pg.quit()
                                        return
                                    self.current_player = "W" if self.current_player == "B" else "B"


            # AI Move
            if self.current_player == "W" and not self.game.game_over():
                move = self.game.get_best_move()
                if move is None:
                    print("No moves available, game is a draw!")
                    pg.quit()
                    return
                row, col = move
                if self.game.board[row][col] == " ":
                    if self.game.make_move(row, col, self.current_player):
                        if self.game.is_win(self.current_player):
                            print(f"{self.current_player} wins!")
                            pg.quit()
                            return
                        self.current_player = "B"

            self.draw_board(self.screen)
            pg.display.flip()
            self.clock.tick(60)
    pg.quit()





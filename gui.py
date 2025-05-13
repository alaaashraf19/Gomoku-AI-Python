import pygame as pg
from pygame.locals import *
from Gomoku import Gomoku

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
        self.screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
        pg.display.set_caption("Gomoku")
        self.font = pg.font.Font(None, 50)
        self.clock = pg.time.Clock()
        self.current_player = "B"

    def draw_board(self, screen):
        board=self.game.board
        screen.fill(LIGHT_BROWN)
        
        # Draw grid lines
        for i in range(BOARD_SIZE):
            pg.draw.line(screen, DARK_BROWN, 
                        (CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE),
                        (WINDOW_SIZE - CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE), 2)
            pg.draw.line(screen, DARK_BROWN, 
                        (CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2),
                        (CELL_SIZE // 2 + i * CELL_SIZE, WINDOW_SIZE - CELL_SIZE // 2), 2)

        # Draw small dots at star points to enhance board appearance (like real Go/Gomoku boards)
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

    def start_menu(self):
        self.screen.fill(LIGHT_BROWN)

        font = pg.font.Font(None, 100)
        text1 = font.render("Gomoku", True, (BLACK))
        rect1 = text1.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
        self.screen.blit(text1, rect1)

        text2 = self.font.render("Choose a color:", True, (BLACK))
        rect2 = text2.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(text2, rect2)

        font = pg.font.Font(None, 25)
        text3 = font.render("(Black starts the game)", True, (BLACK))
        rect3 = text3.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 40))
        self.screen.blit(text3, rect3)

        button1_text = self.font.render("Black", True, (WHITE))
        rectB = button1_text.get_rect(center=(WINDOW_SIZE // 4, WINDOW_SIZE * 3 // 4))
        pg.draw.ellipse(self.screen, BLACK, rectB.inflate(50, 40))
        self.screen.blit(button1_text, rectB)

        button2_text = self.font.render("White", True, (BLACK))
        rectW = button2_text.get_rect(center=(WINDOW_SIZE * 3 // 4, WINDOW_SIZE * 3 // 4))
        pg.draw.ellipse(self.screen, WHITE, rectW.inflate(50, 40))
        self.screen.blit(button2_text, rectW)

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if rectB.collidepoint(mouse_pos):
                        self.human, self.ai = "B", "W"
                    elif rectW.collidepoint(mouse_pos):
                        self.human, self.ai = "W", "B"

                    self.game=Gomoku(BOARD_SIZE, self.human, self.ai)
                    self.run()
                    return
                
            pg.display.flip()
            self.clock.tick(60)

    def run(self):
        winner = None
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
                            if self.game.board[row][col] == " " and self.current_player == self.human:
                                if self.game.make_move((row, col), self.current_player):
                                    if self.game.is_win(self.current_player):
                                        winner = self.current_player
                                    self.current_player = self.ai


            # AI Move
            if self.current_player == self.ai and not self.game.game_over():
                move = self.game.get_best_move()
                if move is None:
                    winner = "D"
                row, col = move
                if self.game.board[row][col] == " ":
                    if self.game.make_move((row, col), self.current_player):
                        if self.game.is_win(self.current_player):
                            winner = self.current_player
                        self.current_player = self.human

            self.draw_board(self.screen)

            if winner == "D":
                text = self.font.render("DRAW!", True, (255, 0, 0))
                rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 10))
                self.screen.blit(text, rect)
            if winner:
                msg = f"{'Human' if winner == self.human else 'AI'} wins!"
                color = BLACK if self.current_player == "W" else WHITE
                text = self.font.render(msg, True, color)
                rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 10))
                self.screen.blit(text, rect)

            pg.display.flip()
            self.clock.tick(60)
    # pg.quit()

import pygame as pg
from pygame.locals import *
from minimax import Gomoku
import tkinter as Tk
from tkinter import messagebox

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
        self.font = pg.font.Font(None, 50)
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
    
    def show_game_over(self,message):
        def retry():
            popup.destroy()
            self.start_menu()
        def exit_game():
            popup.destroy()
            pg.quit()
            exit()
        
        popup=Tk.Tk()
        popup.title("Game Over")
        popup.geometry("300x150")
        popup.resizable(False,False)
        popup.eval('tk::PlaceWindow . center')

        popup.config(bg="#DEB887")

        label = Tk.Label(popup, text=message, font=("Arial", 14), bg="#DEB887", fg="#000000", bd=0, relief="flat")
        label.pack(pady=20)

        button_frame = Tk.Frame(popup,bg="#DEB887")
        button_frame.pack(pady=10)

        retry_button = Tk.Button(button_frame, text="Retry", command=retry, width=10, bg="#A0522D", fg="#FFFFFF", activebackground="#A0522D", activeforeground="#FFFFFF")
        retry_button.pack(side=Tk.LEFT, padx=(10, 20))

        quit_button = Tk.Button(button_frame, text="Quit", command=exit_game, width=10, bg="#A0522D", fg="#FFFFFF", activebackground="#A0522D", activeforeground="#FFFFFF")
        quit_button.pack(side=Tk.LEFT, padx=(10, 20))

        popup.mainloop()

    
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
                            self.game.human, self.game.ai = "B", "W"
                        elif rectW.collidepoint(mouse_pos):
                            self.game.human, self.game.ai = "W", "B"

                        self.game=Gomoku(BOARD_SIZE, self.game.human, self.game.ai)
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
                            if self.game.board[row][col] == " " and self.current_player == self.game.human:
                                if self.game.make_move((row, col), self.current_player):
                                    if self.game.is_win(self.current_player):
                                        winner = self.current_player
                                    self.current_player = self.game.ai

            # AI Move
            if self.current_player == self.game.ai and not self.game.game_over():
                move = self.game.get_best_move()
                if move is None:
                    winner = "Draw"
                row, col = move
                if self.game.board[row][col] == " ":
                    if self.game.make_move(move, self.current_player):
                        if self.game.is_win(self.current_player):
                            winner = self.current_player
                        self.current_player = self.game.human

            self.draw_board(self.screen)
            
            pg.display.flip()
            self.clock.tick(60)

            if winner:
                if winner == "Draw":
                    self.show_game_over("It's a Draw!")
                elif winner == self.game.human:
                    self.show_game_over("You win!")
                else:
                    self.show_game_over("AI wins!")
                return

    #pg.quit()
if __name__ == "__main__":
    gui = GomokuGui()
    gui.start_menu()

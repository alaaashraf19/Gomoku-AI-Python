DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Gomoku:
    def __init__(self, board_size, human, ai):
        self.human = human
        self.ai = ai
        self.n = board_size
        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]
        self.turns=0
    
    def available_moves(self):
        moves = []
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == " ":
                    moves.append(x * self.n + y)
        return moves
    
    def is_on_board(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n
    
    def make_move(self, move, player):
        x, y = move[0], move[1]
        if self.board[x][y] == " ":
            self.board[x][y] = player
            self.turns += 1
            return True
        return False
    
    def count_consequetive_stones(self,x,y,dx,dy,player):
        count=0
        for i in range(5):
            xx = x + i*dx
            yy = y + i*dy
            if not self.is_on_board(xx, yy) or self.board[xx][yy] != player:
                break
            count += 1
        return count

    def evaluate_max_row(self,x,y,dx,dy,player):
        count = self.count_consequetive_stones(x,y,dx,dy,player)

        before_x, before_y = x - dx, y - dy
        after_x, after_y = x + count * dx, y + count * dy

        open_ends = 0
        if self.is_on_board(before_x, before_y) and self.board[before_x][before_y] == " ":
            open_ends += 1
        if self.is_on_board(after_x, after_y) and self.board[after_x][after_y] == " ":
            open_ends += 1

        if count == 5:
            return 100000
        elif count == 4:
            if open_ends == 2:
                return 10000
            elif open_ends == 1:
                return 1000
        elif count == 3:
            if open_ends == 2:
                return 1000
            elif open_ends == 1:
                return 100
        elif count == 2:
            if open_ends == 2:
                return 100
            elif open_ends == 1:
                return 10
        elif count == 1:
            if open_ends == 2:
                return 10
            elif open_ends == 1:
                return 1
        return 0
    
    def evaluate_board(self):
        total=0
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] != " ":
                    for dx, dy in DIRECTIONS:
                        if self.board[x][y] == self.ai:
                            total += self.evaluate_max_row(x, y, dx, dy, self.board[x][y])
                        elif self.board[x][y] == self.human:
                            total -= self.evaluate_max_row(x, y, dx, dy, self.board[x][y])
        return total

    def is_win(self,player):
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == player:
                    for dx, dy in DIRECTIONS:
                        if self.count_consequetive_stones(x, y, dx, dy, player) == 5:
                            return True
        return False

    def get_neighbors(self):
        neighbors = set()
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] != " ":
                    for dx in range(-1, 2):# direction of x is either -1 or 1 or 0 
                        for dy in range(-1, 2): 
                            xx, yy = x + dx, y + dy
                            if self.is_on_board(xx, yy) and self.board[xx][yy] == " ":
                                neighbors.add((xx, yy))
        if not neighbors:
            return {(self.n // 2, self.n // 2)} #tel3b fl middle 
        return neighbors
    
    def minimax(self, depth, isMax):
        #return bestMove, score
        if self.is_win(self.ai):
            return None, 1000000
        if self.is_win(self.human):
            return None, -1000000
        if depth == 0 or self.turns >= self.n * self.n :
            return None, self.evaluate_board() #no best move and return score
        
        moves = list(self.get_neighbors())
        best_move = None

        if isMax:
            maxScore = float("-inf")
            for (x,y) in moves:
                self.board[x][y] = self.ai
                self.turns += 1
                score=self.minimax(depth - 1, False)[1]
                
                #score = self.minimax(depth +1, False)
                self.board[x][y] = " "
                self.turns -= 1
                if score > maxScore:
                    maxScore = score
                    best_move = (x, y)   
            return best_move, maxScore  
        
        else:
            minscore = float("inf")
            for (x,y) in moves:
                self.board[x][y] = self.human
                self.turns += 1
                score=self.minimax(depth - 1, True)[1]
                
                #score = self.minimax(depth +1, False)
                self.board[x][y] = " "
                self.turns -= 1
                if score < minscore:
                    minscore = score
                    best_move = (x, y)   
            return best_move, minscore  
        
    def get_best_move(self):
        best_move, best_score =self.minimax(3, True)
        if best_move is None:
            return None
        # print("Score is:", best_score)
        return best_move

    def game_over(self):
        return self.turns >= self.n * self.n or self.is_win(self.ai) or self.is_win(self.human)
    
    def print_board(self):
        # Print column letters header: a b c ... o (assuming n=15)
        print("  ", end="")
        for col in range(self.n):
            print(chr(ord('a') + col) + " ", end="")
        print()

        for row in range(self.n):
            # Print row letter at the start of each row
            print(chr(ord('a') + row) + " ", end="")

            for col in range(self.n):
                # Print the stone or empty space
                print(self.board[row][col], end="")

                # Print "-" between columns except after last column
                if col != self.n - 1:
                    print("-", end="")

            print()  # Move to next line after each row

            # Print "| " connectors between rows except after last row
            if row != self.n - 1:
                print("  ", end="")
                for col in range(self.n):
                    print("| ", end="")
                print()

    def play_game(self):
        ai_turn = (self.ai == "B")

        while not self.game_over():
            self.print_board()
            if ai_turn:
                print("\n<<AI turn>>")
                move = self.get_best_move()
                if move is None:
                    print("No moves available, game is a draw!")
                    break
                letterRow = chr(move[0] + ord('a'))
                letterCol = chr(move[1] + ord('a'))
                print("AI played at:", letterRow, letterCol)
                self.make_move(move, self.ai)
            else:
                print("\n<<Your turn>>")
                while True:
                    try:
                        moveRow, moveCol = input("Enter a spot of two letters: ").split()
                        moveRow = ord(moveRow) - ord('a')
                        moveCol = ord(moveCol) - ord('a')
                        move = (moveRow, moveCol)

                        if self.is_on_board(moveRow, moveCol) and self.make_move(move, self.human):
                            break
                        else:
                            print("Invalid move!! Try again")
                    except ValueError:
                        print("Input not valid!! Enter two letters seperated")
            ai_turn = not ai_turn

        self.print_board()
        winner_ai = self.is_win(self.ai)
        winner_human = self.is_win(self.human)
        if winner_ai:
            print("\nCongrats!! You win!")
        elif winner_human:
            print("\nAI wins!")
        else:
            print("\nDraw!")

if __name__ == "__main__":
    print("Welcome to Gomoku!!")
    print("Black plays first, and White plays second")
    print("Choose your character (Enter 1 or 2):")
    print("(1)Black")
    print("(2)White")
    while True:
            try:
                turn = int(input())
                if turn not in (1, 2):
                    print("Invalid input. Enter 1 or 2.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number (1 or 2).")
    print("You are playing as Black" if turn == 1 else "You are playing as White")
    print("AI is playing as White" if turn == 1 else "AI is playing as Black")
    human = "B" if turn == 1 else "W"
    ai = "W" if turn == 1 else "B"

    game = Gomoku(15, human, ai)
    game.play_game()

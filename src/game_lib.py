class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    
    def display_board(self):
        for row in self.board:
            print("".join(map(str, row)))

    def update_board(self, pos):
        row = (pos-1) // 3 
        col = (pos-1) % 3

        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
        else:
            print("That place is already taken. Please choose another.") 
        
    def check_win(self):
        for i in range(3):
            row_win = True
            for j in range(3):
                if self.board[i][j] != self.current_player:
                    row_win = False
                    break
            if row_win:
                return True

        for i in range(3):
            col_win = True
            for j in range(3):
                if self.board[j][i] != self.current_player:
                    col_win = False
                    break
            if col_win:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player: 
            return True

        return False 

    def check_draw(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True  

    def switch_player(self): 
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def game(self): 
        while True: 
            self.display_board()
            pos = int(input(f"Player {self.current_player}, enter a number between 1 and 9: "))
            if pos < 1 or pos > 9:
                print("Enter a number between 1 and 9")
                continue
            self.update_board(pos)

            if self.check_win() == True:
                self.display_board()
                winner = "Player 1" if self.current_player == 'X' else "Player 2"
                print("The winner is " + winner)
                break

            if self.check_draw():
                self.display_board()
                print("Draw!")
                break

            self.switch_player()
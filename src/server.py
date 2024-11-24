import socket
#import threading
import sys
from game_lib import TicTacToe

class Server:
    
    def __init__(self, host: str = socket.gethostbyname(socket.gethostname()), port: int = 12345):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.running = False
        self.connections = []

    def handle_game(self):
        game = TicTacToe()
        player_turn = 0  # 0 for Player 1 (X), 1 for Player 2 (O)

        while True:
            current_conn = self.connections[player_turn]
            opponent_conn = self.connections[1 - player_turn]

            # Send the game board to the current player
            board_state = "\n".join([" | ".join(row) for row in game.board]) + "\n"
            current_conn.sendall(f"Your turn, Player {game.current_player}:\n{board_state}".encode())

            # Receive the player's move
            try:
                pos = int(current_conn.recv(1024).decode().strip())
            except ValueError:
                current_conn.sendall("Invalid input. Please send a number between 1 and 9.\n".encode())
                continue

            # Validate and update the board
            row, col = (pos - 1) // 3, (pos - 1) % 3
            if game.board[row][col] != ' ':
                current_conn.sendall("Invalid move. Spot already taken.\n".encode())
                continue

            game.update_board(pos)

            # Check for win/draw
            if game.check_win():
                for conn in self.connections:
                    conn.sendall(f"Player {game.current_player} wins!\n".encode())
                break
            elif game.check_draw():
                for conn in self.connections:
                    conn.sendall("It's a draw!\n".encode())
                break

            # Switch turns
            game.switch_player()
            player_turn = 1 - player_turn

        # Close connections after the game
        for conn in self.connections:
            conn.close()
        self.socket.close()

    def start(self):
        # Start server and start listening for connections
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.socket.settimeout(60) # timeout of 60 seconds
        self.running  = True

        print(f"Server is running on {self.host}:{self.port}")
        print("Waiting for players to connect...")

        # Wait for two players
        while len(self.connections) < 2:
            conn, addr = self.socket.accept()
            self.connections.append(conn)
            print(f"Player {len(self.connections)} connected from {addr}")

        print("Both players are connected. Starting the game!")

        self.handle_game()

        print("Game over. Server shutting down.")


    def shutdown(self):
        print("\n")
        print("Shutting down server...")
        self.running = False
        self.socket.close()
        sys.exit(0)








if __name__ == "__main__":
    server = Server()
    server.start()

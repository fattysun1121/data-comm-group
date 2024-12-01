import socket
import threading
import time
import sys
from game_lib import TicTacToe
import constants
class Server:
   
    def __init__(self, host: str = socket.gethostbyname(socket.gethostname())):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket for game hosting
        self.host = host
        self.port = 6003
        self.running = False
        self.connections = []

    # Announce server information to interested clients
    def multicast_announcement(self):
        multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        
        message = f"Game Server|IP:{socket.gethostbyname(socket.gethostname())}|Port:{self.port}"
        print(f"Broadcasting: {message}")
        try:
            while True:
                multicast_sock.sendto(message.encode('utf-8'), (constants.MCAST_GRP, constants.MCAST_PORT))
                
                time.sleep(2)
        except KeyboardInterrupt:
            multicast_sock.close()
            print(f"Broadcast ended.")
        
    def host_game(self):
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
        try:
            # Start a thread to broadcast server information
            multicast_thread = threading.Thread(target=self.multicast_announcement, daemon=True)
            multicast_thread.start()

            # Start server and start listening for connections
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)  # only 2 players are required, the rest will be in a queue
            self.running  = True

            print(f"Server is running on {self.host}:{self.port}")
            print("Waiting for players to connect...")
            while True:
                # Wait for two players
                while len(self.connections) < 2:
                    conn, addr = self.socket.accept()
                    self.connections.append(conn)
                    print(f"Player {len(self.connections)} connected from {addr}")

                print("Both players are connected. Starting the game!")

                self.host_game()
        except KeyboardInterrupt:
            self.socket.close()
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

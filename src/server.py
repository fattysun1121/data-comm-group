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
        self.port = 6001
        self.connections = []
        self.game_start = False
        self.connection_mutex = threading.Lock()
        self.winner_score = 0
        self.last_winner = None
        self.timer = None


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
        if len(self.connections) < 2:   # waits until at least two clients are connected
            print("Not enough players to start the game.")
            return
        
        game = TicTacToe()
        player_turn = 0  # 0 for Player 1 (X), 1 for Player 2 (O)
        draw = False

        while True:
            if player_turn >= len(self.connections):
                print(f"Invalid turn index {player_turn}. Ending game.")
                break

            current_conn = self.connections[player_turn]

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
                if self.last_winner != game.current_player:
                    self.winner_score = 0
                
                self.winner_score += 1
                for i in range(2):
                    self.connections[i].sendall(f"Player {game.current_player} wins!\n".encode())
                    self.connections[i].sendall(f"Player {game.current_player}'s score: {self.winner_score}".encode())

                    self.last_winner = game.current_player # update the winner
                break
            elif game.check_draw():
                for i in range(2):
                    self.connections[i].sendall("It's a draw!\n".encode())
                    self.connections[i].sendall("Rematch!\n".encode())
                draw = True
                break

            # Switch turns
            game.switch_player()
            player_turn = 1 - player_turn

        # Close the loser's connection and kick them off the connection list
        if not draw:
            self.connection_mutex.acquire()
            # When someone wins, player_turn stores the winner, 1 - player_turn is the loser
            self.connections[1 - player_turn].close()
            del self.connections[1 - player_turn]
            self.connection_mutex.release()
        # When draw, do a rematch

    def connect_player(self):
        # Wait for two players
        while True:
            self.connection_mutex.acquire()
            if len(self.connections) >= 2:
                self.game_start = True
            else:
                self.game_start = False
            self.connection_mutex.release()
            conn, addr = self.socket.accept()
            self.connection_mutex.acquire()
            self.connections.append(conn)
            print(f"Player {len(self.connections)} connected from {addr}")
            self.connection_mutex.release()

    
    def start(self):
        try:
            # Start a thread to broadcast server information
            multicast_thread = threading.Thread(target=self.multicast_announcement, daemon=True)
            multicast_thread.start()

            # Start server and start listening for connections
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)  # only 2 players are required, the rest will be in a queue

            print(f"Server is running on {self.host}:{self.port}")
            print("Waiting for players to connect...")

            connection_thread = threading.Thread(target=self.connect_player, daemon=True)
            connection_thread.start()
            while True:
                if len(self.connections) < 2:
                    self.start_timer(timeout=30)
                    while True:
                        print("Waiting for more players to connect...\n")
                        time.sleep(2)
                        if self.check_time():
                            self.check_shutdown()
                        
                else:
                    self.reset_timer()

                if self.game_start:
                    print("Starting game...")
                    self.host_game()
                    print("Game ended")
            
        except KeyboardInterrupt:
            self.socket.close()
            print("Game over. Server shutting down.")


    def shutdown(self):
        print("\n")
        print("Shutting down server...")
        self.socket.close()
        sys.exit(0)
    
        # Timer functions
    def start_timer(self, timeout): #Start timer
        if self.timer: #Cancel any existing timer
            self.timer.cancel()
        self.timer_start_time = time.time()
        self.timeout = timeout
        self.timer = threading.Timer(timeout, self.check_shutdown)
        self.timer.start()
        print(f"Timer started for {timeout} seconds.")
    
    def check_time(self):
        if self.timer_start_time is None:
            return False
        passed_time = time.time() - self.timer_start_time
        return passed_time > self.timeout
    
    def check_shutdown(self): #Check server and if there are no players, shut it down
        if not self.connections:
            print("No players connected. Shutting down the server due to inactivity.")
            self.shutdown()
        else:
            print("Player(s) are connected. Server will remain active.")
    
    def reset_timer(self): #Reset timer if players connect
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
            self.timer = None


if __name__ == "__main__":
    server = Server()
    server.start()

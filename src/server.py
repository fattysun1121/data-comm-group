import socket
import threading
import sys
from game_lib import TicTacToe

class Server:
    
    def __init__(self, host: str = socket.gethostbyname(socket.gethostname()), port: int = 12345):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.running = False


    def start(self):
        # Start server and start listening for connections
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.socket.settimeout(1)
        self.running  = True

        print(f"Server is running on {self.host}:{self.port}")
        print("Waiting for players to connect...")

        connections = []
        addresses = []

        try:
            while len(connections) < 2 and self.running:
                try:
                    conn, addr = self.socket.accept()
                    if len(connections) < 2:
                        print(f"Player {len(connections) + 1} connected from {addr}")
                        connections.append(conn)
                        addresses.append(addr)
                    else:
                        conn.sendall("Server is full. Please try again later.\n".encode())
                        conn.close()
                except socket.timeout:
                    continue  # Continue waiting for connections
        except KeyboardInterrupt:
            self.shutdown()

        print("Both players are connected. Starting the game!")

        # Initialize the Tic Tac Toe game
        game = TicTacToe()

        # TODO: Play game + Communicating game state

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

import socket
import threading
from game_lib import TicTacToe

class Server:
    
    def __init__(self, host: str = socket.gethostbyname(socket.gethostname()), port: int = 12345):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port


    def start(self):
        # Start server and start listening for connections
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)

        print(f"Server is running on {self.host}:{self.port}")
        print("Waiting for players to connect...")

        connections = []
        addresses = []

        # Accept connections
        while len(connections) < 2:
            conn, addr = self.socket.accept()
            if len(connections) < 2:
                print(f"Player {len(connections) + 1} connected from {addr}")
                connections.append(conn)
                addresses.append(addr)
            else:
                # Deny further connections with a message
                conn.sendall("Server is full. Please try again later.\n".encode())
                conn.close()

        print("Both players are connected. Starting the game!")

        # Initialize the Tic Tac Toe game
        game = TicTacToe()

        # TODO: Play game + Communicating game state

        print("Game over. Server shutting down.")


if __name__ == "__main__":
    server = Server()
    server.start()

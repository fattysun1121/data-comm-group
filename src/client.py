import socket

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self, host: str, port: int):
        # Connect the client_socket_socket to the server using the provided host and port
        self.socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            try:
                # Receive messages from the server
                message = self.socket.recv(1024).decode()
                print(message)

                if "Your turn" in message:
                    move = input("Enter your move (1-9): ")
                    self.socket.sendall(move.encode())
                elif "wins!" in message or "draw" in message:
                    print("Game over!")
                    break
            except ConnectionResetError:
                print("Server connection lost.")
                break

        self.socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()

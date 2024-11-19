import socket

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self, host: str, port: int):
        # Connect the client_socket_socket to the server using the provided host and port
        self.socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # TODO: code for what client receives as message to play game and see game state


if __name__ == "__main__":
    client = Client()
    client.start()

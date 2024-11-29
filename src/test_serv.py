import socket
import time
import threading

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5007
GAME_PORT = 6001

# Multicast announcement function
def multicast_announcement():
    multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    
    message = f"Game Server|IP:{socket.gethostbyname(socket.gethostname())}|Port:{GAME_PORT}"
    while True:
        multicast_sock.sendto(message.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
        print(f"Broadcasting: {message}")
        time.sleep(2)

# Game hosting function
def game_host():
    game_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game_sock.bind(("", GAME_PORT))
    game_sock.listen(5)  # Allow up to 5 simultaneous connections
    print(f"Game server running on port {GAME_PORT}")

    while True:
        client, addr = game_sock.accept()
        print(f"New connection from {addr}")
        client.send(b"Welcome to the game!")
        client.close()

# Run multicast and game hosting in separate threads
multicast_thread = threading.Thread(target=multicast_announcement, daemon=True)
game_thread = threading.Thread(target=game_host, daemon=True)

multicast_thread.start()
game_thread.start()

try:
    multicast_thread.join()
    game_thread.join()
except KeyboardInterrupt:
    print("Server shutting down.")
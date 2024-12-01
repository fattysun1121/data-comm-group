import socket
import threading
import struct
import constants

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_mutex = threading.Lock()
        self.servers = {}  # for checking duplicate servers and storing server information
        self.serv_list = []  # for indexing servers

    # Multicast receiver to discover servers
    def discover_servers(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(("", constants.MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(constants.MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Listening for game servers...")
        
        while True:
            data, addr = sock.recvfrom(1024)
            if self.servers.get(addr, 0) == 0: 
                self.serv_mutex.acquire()
                self.servers[addr] = data.decode('utf-8')  # decode byte to string
                self.serv_list.append(addr)
                self.serv_mutex.release()          
                print(f"Discovered server: {data.decode('utf-8')} from {addr}")

    def start(self):
        discover_thread = threading.Thread(target=self.discover_servers, daemon=True)
        discover_thread.start()
        
        # Discover and connect to server 
        try:
            while True:
                self.serv_mutex.acquire()

                for i, serv in enumerate(self.serv_list):
                    print(f'Server Number #{i}: {serv}')

                self.serv_mutex.release()

                cmd = input("Enter 'connect <server number>' to join a server or 'display' to see available servers: ").strip()
                if cmd.startswith("connect"):
                    _, serv_num = cmd.split()
                    serv_num = int(serv_num)
                    # parse server
                    
                    serv_info = self.servers[self.serv_list[serv_num]]  
                    print(serv_info)
                    ip = serv_info.split("|")[1].split(":")[1]
                    port = serv_info.split("|")[2].split(":")[1]
                    self.socket.connect((ip, int(port)))
                    print(f"Connected to server at {ip}:{port}")
                    break
                elif cmd.startswith("display"):
                    continue
        

            # Run game after connection is made        
            while True:
                try:
                    # Receive messages from the server
                    message = self.socket.recv(1024).decode()
                    print(message)

                    if "Your turn" in message:
                        move = input("Enter your move (1-9): ")
                        self.socket.sendall(move.encode())
                    elif "wins!" in message:
                        print("Game over!")
                except ConnectionResetError:
                    print("Server connection lost.")
                    break
        except KeyboardInterrupt:
            self.socket.close()
            print("Client shutting down.")
        finally:
            self.socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()

import socket
import struct
import threading

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5007

mutex = threading.Lock()  # Lock for accessing servers and server_list
servers = {}
server_list = []
# Multicast receiver to discover servers
def discover_servers():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Listening for game servers...")
    
    while True:
        data, addr = sock.recvfrom(1024)
        if servers.get(addr, 0) == 0: 
          mutex.acquire()
          servers[addr] = data.decode('utf-8')  # decode byte to string
          server_list.append(addr)
          mutex.release()          
          print(f"Discovered server: {data.decode('utf-8')} from {addr}")

# Connect to a discovered server
def connect_to_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(sock.recv(1024).decode('utf-8'))
    sock.close()

# Discover servers and manually connect to one
discover_thread = threading.Thread(target=discover_servers, daemon=True)
discover_thread.start()


try:
    while True:
        mutex.acquire()

        for i, serv in enumerate(server_list):
          print(f'Server Number #{i}: {serv}')

        mutex.release()

        cmd = input("Enter 'connect <server number>' to join a server or 'display' to see available servers: ").strip()
        if cmd.startswith("connect"):
            _, serv_num = cmd.split()
            serv_num = int(serv_num)
            # parse server
            
            serv_info = servers[server_list[serv_num]]  
            print(serv_info)
            ip = serv_info.split("|")[1].split(":")[1]
            port = serv_info.split("|")[2].split(":")[1]
            connect_to_server(ip, int(port))
        elif cmd.startswith("display"):
            continue
except KeyboardInterrupt:
    print("Client shutting down.")
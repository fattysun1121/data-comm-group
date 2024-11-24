from server import Server
from client import Client
import sys

def main():
    while True:
        entity = input("Do you wish to start running a client process or a server process on this device: ")
        if entity not in  ['client', 'server']:
            print("Invalid input. \n")
        elif entity == 'server':
            process = Server()
            process.start()
            break
        elif entity == 'client':
            process = Client()
            process.start("127.0.1.1", 12345)
            break
    print("Exiting Process...")
    sys.exit()

if __name__ == "__main__":
    main()
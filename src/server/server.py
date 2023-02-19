from server_structs import *
import socket
from _thread import *
import threading


class Server:
    data_structure = RoutingInfoDataStructure()

    # creates and handles all connections to the server on individual threads
    def threadHandler(self):
        try:
            s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_sock.bind((SERVER_ADDR, PORT))
            s_sock.listen()
            print("[LISTENING]...")
        except socket.error as perror:
            print("Could not create socket due to: ", perror)
        
        while True:
            try:
                client, peer_addr = s_sock.accept()
                request_type = client.recv(1024).decode()

                if request_type == "register file(s)":
                    thread = threading.Thread(target=self.receivePublicFiles, args=(client, peer_addr))
                    thread.start()
                    print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)
            except socket.error as perror:
                print(f"Could not accept connections from {peer_addr} due to {perror}")

    # receives all publicly made available files and stores their routing info
    def receivePublicFiles(self, client:socket, peer_addr):
        print(f"[NEW CONNECTION] {peer_addr} connected")

        files = []
        file_count = 0
        connected = True

        while connected:
            number_of_files = int(client.recv(1024).decode())
            
            while file_count < number_of_files:
                files.append(File(client.recv(1024).decode(), int(client.recv(1024).decode())))
                file_count += 1

            self.data_structure.createDataStructure(files, peer_addr)
        


server = Server()
server.threadHandler()

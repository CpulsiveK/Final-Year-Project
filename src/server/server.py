from server_structs import *
import socket
from _thread import *
import threading
import struct


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
            except socket.error as perror:
                print(f"Could not accept connections from {peer_addr} due to {perror}")
            
            byte_size_of_request_type = client.recv(4)
            buffer_size = struct.unpack('!I', byte_size_of_request_type)[0]
            request_type = client.recv(buffer_size).decode()
            print(request_type)

            if request_type == "makeFilePublic":
                thread = threading.Thread(target=self.receivePublicFiles, args=(client, peer_addr))
                thread.start()
                print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)

    # receives all publicly made available files and stores their routing info
    def receivePublicFiles(self, client:socket.SocketType, peer_addr):
        print(f"[NEW CONNECTION] {peer_addr} connected")

        byte_size_number_of_files = client.recv(4)
        number_of_files_buffer_size = struct.unpack('!I', byte_size_number_of_files)[0]
        number_of_files = client.recv(number_of_files_buffer_size).decode()
        print(number_of_files)

        random = client.recv(1024).decode()
        print(random)
        
        # files = []
        # file_count = 0
        # connected = True

        # while connected:
        #     number_of_files = int(client.recv(1024).decode())
            
        #     while file_count < number_of_files:
        #         files.append(File(client.recv(1024).decode(), int(client.recv(1024).decode())))
        #         file_count += 1

        #     self.data_structure.createDataStructure(files, peer_addr)
        


server = Server()
server.threadHandler()

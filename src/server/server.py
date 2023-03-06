from server_structs import *
import struct


class Server:
    data_structure = RoutingInfoDataStructure()

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
            
            byte_size_of_makeFilePublic_request = client.recv(4)
            makeFilesPublic_buff_size = struct.unpack('!I', byte_size_of_makeFilePublic_request)[0]
            makeFilePublic_request = client.recv(makeFilesPublic_buff_size).decode()
            print(makeFilePublic_request)

            if makeFilePublic_request == "makeFilePublic":
                createThread(self.storeReceivedPublicFiles, (client, peer_addr))

    def storeReceivedPublicFiles(self, client:socket.SocketType, peer_addr):
        connected_peer = socket.gethostbyaddr(peer_addr[0])
        print(f"[NEW CONNECTION] {peer_addr[0]}[{connected_peer[0]}] connected")

        files = []

        byte_size_num_of_files = client.recv(4)
        buff_size_of_num_of_files = struct.unpack('!I', byte_size_num_of_files)[0]
        num_of_files = client.recv(buff_size_of_num_of_files).decode()
        num_of_files = int(num_of_files)

        i = 0

        while i < num_of_files:
            byte_size_of_file_name = client.recv(4)
            buff_size_of_file_name = struct.unpack('!I', byte_size_of_file_name)[0]
            file_name = client.recv(buff_size_of_file_name).decode()
            print(f"received file name {file_name}")

            byte_size_of_file_size = client.recv(4)
            buff_size_of_file_size = struct.unpack('!I', byte_size_of_file_size)[0]
            file_size = client.recv(buff_size_of_file_size).decode()
            file_size = int(file_size)
            print(f"received file size {file_size}")

            files.append(File(file_name, file_size))

            i += 1
        
        self.data_structure.createDataStructure(files, peer_addr[0])

        print(self.data_structure.routing_info)
        
        


server = Server()
server.threadHandler()

from server_structs import *
import struct


class Server:
    data_structure = RoutingInfoDataStructure()

    def threadHandler(self, client:socket.SocketType, peer_addr):
        byte_of_request_type = client.recv(4)
        buff_size = struct.unpack('!I', byte_of_request_type)[0]
        request_type = client.recv(buff_size).decode()
        print(request_type)

        if request_type == "makeFilePublic":
            self.storeReceivedPublicFiles(client, peer_addr)
        elif request_type == "searchFiles":
            self.returnSearchedFiles(client, peer_addr)


    def startServer(self):
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
            
            thread = threading.Thread(target=self.threadHandler, args=(client, peer_addr))
            thread.start()
            print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)


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

            file = File(file_name, file_size)
            files.append(file)

            i += 1
        
        self.data_structure.createDataStructure(files, peer_addr[0])
        print(self.data_structure.routing_info)
            

    def returnSearchedFiles(self, client:socket.SocketType, peer_addr):
        connected_peer = socket.gethostbyaddr(peer_addr[0])
        print(f"[NEW CONNECTION] {peer_addr[0]}[{connected_peer[0]}] connected")

        byte_of_len_of_filename = client.recv(4)
        buff_size_of_filename = struct.unpack('!I', byte_of_len_of_filename)[0]
        filename = client.recv(buff_size_of_filename).decode()
        print("received ", filename)

        byte_of_len_of_filesize = client.recv(4)
        buff_size_of_filesize = struct.unpack('!I', byte_of_len_of_filesize)[0]
        filesize = client.recv(buff_size_of_filesize).decode()
        filesize = int(filesize)
        print("received ", filesize)

        file = File(filename, filesize)

        result = self.data_structure.search(file)
        print(result)
        

        


server = Server()
server.startServer()

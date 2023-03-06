from peers_structs import *
import socket
import struct


class Client:
    def makeFilesPublic(self, files:list[File]):
        num_of_files = str(len(files)).encode()
        byte_size_of_num_of_files = struct.pack('!I', len(num_of_files))

        request_type = "makeFilePublic".encode()
        byte_size_of_request_type = struct.pack('!I', len(request_type))

        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p_sock.connect((SERVER_ADDR, PORT))
            print("connecting...")
        except socket.error as perror:
            print("Couldn't create socket due to ", perror)

        p_sock.sendall(byte_size_of_request_type)
        p_sock.sendall(request_type)
        
        p_sock.sendall(byte_size_of_num_of_files)
        p_sock.sendall(num_of_files)
        
        for i in range(len(file)):
            try:
                byte_size_of_file_name = struct.pack('!I', len(str(file[i].file_name)))
                p_sock.sendall(byte_size_of_file_name)
                p_sock.send(str(file[i].file_name).encode())

                byte_size_of_file_size = struct.pack('!I', len(str(file[i].file_size)))
                p_sock.sendall(byte_size_of_file_size)
                p_sock.send(str(file[i].file_size).encode())
            except socket.error as perror:
                print("Could not send data due to ", perror)
        
        p_sock.close()
    



file = [File("COE 152", 23), File("Computer Networks", 45)]

peer = Client()
peer.makeFilesPublic(file)

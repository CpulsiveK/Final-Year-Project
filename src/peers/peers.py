from peers_structs import *
import socket
from sys import getsizeof
import struct


class Client:
    def makeFilePublic(self, file:list[File]):
        number_of_files = str(len(file)).encode()
        byte_size_of_number_of_files = struct.pack('!I', len(number_of_files))

        request_type = "makeFilePublic".encode()
        byte_size_of_request_type = struct.pack('!I', len(request_type))

        # create a socket and send the number of files the server should expect
        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p_sock.connect((SERVER_ADDR, PORT))
            print("connecting...")
        except socket.error as perror:
            print("Couldn't create socket due to ", perror)

        p_sock.sendall(byte_size_of_request_type)
        p_sock.sendall(request_type)
        
        p_sock.sendall(byte_size_of_number_of_files)
        p_sock.sendall(number_of_files)
        p_sock.send("hello".encode())
        
        # for i in range(len(f ile)):
        #     try:
        #         p_sock.send(str(file[i].file_name).encode())
        #         p_sock.send(str(file[i].file_size).encode())
        #     except socket.error as perror:
        #         print("Could not send data due to ", perror)

file = [File("COE 152", 23), File("Computer Networks", 45)]

peer = Client()
peer.makeFilePublic(file)
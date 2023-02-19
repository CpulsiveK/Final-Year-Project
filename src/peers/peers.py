from peers_structs import *
import socket


class Client:
    def makeFilePublic(self, file:list[File]):
        number_of_files = len(file)
        request_type = "makeFilePublic"

        # create a socket and send the number of files the server should expect
        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p_sock.connect((SERVER_ADDR, PORT))
            print("connecting...")
            p_sock.send(request_type.encode())
            p_sock.send(str(number_of_files).encode())
        except socket.error as perror:
            print("Couldn't create socket due to ", perror)
        
        for i in range(len(file)):
            try:
                p_sock.send(str(file[i].file_name).encode())
                p_sock.send(str(file[i].file_size).encode())
            except socket.error as perror:
                print("Could not send data due to ", perror)

file = [File("COE 152", 23), File("Computer Networks", 45)]

peer = Client()
peer.makeFilePublic(file)
from peers_structs import *
import socket


class Client:
    def makeFilePublic(self, file:list[File]):
        number_of_files = len(file)

        # create a socket and send the number of files the server should expect
        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p_sock.connect((SERVER_ADDR, PORT))
            print("connecting...")
            p_sock.send(str(number_of_files).encode())
        except socket.error as e:
            print("Couldn't create socket due to ", e)
        
        for i in range(len(file)):
            try:
                p_sock.send(str(file[i].file_name).encode())
                p_sock.send(str(file[i].file_size).encode())
            except socket.error as e:
                print("Could not send data due to ", e)

file = [File("COE 152", 23), File("Computer Networks", 45)]

peer = Client()
peer.makeFilePublic(file)
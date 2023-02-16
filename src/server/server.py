from server_structs import *
import socket


class Server:
    def receivePublicFiles(self):
        try:
            s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_sock.bind((SERVER_ADDR, PORT))
            s_sock.listen()
        except socket.error as perror:
            print("Could not create socket due to: ", perror)
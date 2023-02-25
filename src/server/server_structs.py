from _thread import *
import threading
import socket

SERVER_ADDR = socket.gethostbyname("localhost")
print(SERVER_ADDR)
PORT = 5050

class File:
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size

class RoutingInfoDataStructure:
    routing_info = []
    shared_files_info = {}

    def createDataStructure(self, files:list[File], peer_addr:str):
        self.shared_files_info[peer_addr] = files
        self.routing_info.append(self.shared_files_info)


def thread(function, args: tuple):
    thread = threading.Thread(target=function, args=args)
    thread.start()
    print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)
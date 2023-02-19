import socket

SERVER_ADDR = socket.gethostbyname("localhost")
print(SERVER_ADDR)
PORT = 5050

# represent a file in the network layer
class File:
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size

# creates a data structure to store the routing information of files
class RoutingInfoDataStructure:
    routing_info = []

    def createDataStructure(self, files:list[File], peer_addr:str):
        is_populated = False

        while is_populated == False:
            shared_files_info = {}
            shared_files_info[peer_addr] = files
            self.routing_info.append(shared_files_info)
            is_populated = True
SERVER_ADDR = "127.0.0.1"
PORT = 5050


class File:
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size


class RoutingInfoDataStructure:
    routing_info = []

    def createDataStructure(self, files:list[File], peer_addr:str):
        is_populated = False

        while is_populated == False:
            shared_files_info = {}
            shared_files_info[peer_addr] = files
            self.routing_info.append(shared_files_info)
            is_populated = True
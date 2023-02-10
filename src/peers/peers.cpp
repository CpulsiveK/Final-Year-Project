#include <fstream>
#include "peers.hpp"

// used to lock certain parts of code
std::mutex mtx;
// defines the socket structure
struct sockaddr_in server_address;


int Client::chunkNumber(uint32_t file_length){
    int chunk_number = file_length/CHUNK_SIZE;

    // round up result
    if((CHUNK_SIZE * chunk_number) < file_length){
        chunk_number += 1;
    }

    return chunk_number;
}


int Client::makeFilePublic(uint16_t number_of_files, std::vector<fileInfo> file_info){
    int peerSocket = socket(AF_INET, SOCK_STREAM, 0);
    char receiveMessage[100] = {};
    uint32_t file_length = 0;
    std::string file_name;
    // The available option in commands
    const uint32_t request_type = 0;
    uint16_t port = PORT;
    std::string response_message;

    // create socket
    if(peerSocket < 0){
        perror("Failed to create socket");
        exit(0);
    }

    // connects to the server
    if (connect(peerSocket, (struct sockaddr*) &server_address, sizeof(server_address)) < 0){
        perror("Failed to connect");
        exit(0);
    }

    // below registers the file a peer wants to share
    send(peerSocket, &request_type, sizeof(request_type), 0);
    send(peerSocket, &port, sizeof(port), 0);
    send(peerSocket, &number_of_files, sizeof(number_of_files), 0);

    for(int i=0; i<number_of_files; i++){
        send(peerSocket, &file_info[i].file_name, sizeof(file_info[i].file_name), 0);
        send(peerSocket, &file_info[i].file_length, sizeof(file_info[i].file_length), 0);
    }

    if(recv(peerSocket, &response_message, sizeof(response_message), 0) < 0){
        perror("Server response failed");
        return -1;
    }

    std::cout << "server response: " << response_message << std::endl;
    close(peerSocket);

    return 0;
}


int Client::requestFileAvailable(){
    int peerSocket = socket(AF_INET, SOCK_STREAM, 0);
    const uint32_t request_type = 1;
    uint16_t number_of_files;
    std::string file_name;
    uint32_t file_length;

    if(peerSocket < 0){
        perror("Failed to create socket");
        exit(0);
    }

    // get files a client can download
    send(peerSocket, &request_type, sizeof(request_type), 0);
    send(peerSocket, &number_of_files, sizeof(number_of_files), 0);

    for(int i=0; i<number_of_files; i++){
        recv(peerSocket, &file_name, sizeof(file_name), 0);
        recv(peerSocket, &file_length, sizeof(file_length), 0);
        std::cout << file_name << ": " << file_length << " bytes";

        if (i != number_of_files - 1){
            std::cout << ", ";
        }
    }
    close(peerSocket);

    return 0;
}


int Client::requestFileLocation(std::string file_name, std::vector<chunk> &chunks, int &file_size){
    int peerSocket = socket(AF_INET, SOCK_STREAM, 0);
    // received info from server
    const uint32_t request_type = 2;
    uint16_t number_of_locations;
    uint16_t number_of_chunks;
    uint32_t ip_address;
    uint16_t port;
    struct in_addr temp_address;
    uint32_t chunk_index;
    uint32_t file_length;
    struct chunk temp_chunk;
    struct peer temp_peer;

    if(peerSocket < 0){
        perror("Failed to create socket");
        exit(0);
    }

    if(connect(peerSocket, (struct sockaddr*) &server_address, sizeof(server_address)) < 0){
        perror("Failed to connect to server");
        exit(0);
    }

    // ask server for peers having the file
    send(peerSocket, &request_type, sizeof(request_type), 0);
    send(peerSocket, &file_name, sizeof(file_name), 0);
    recv(peerSocket, &number_of_locations, sizeof(number_of_locations), 0);

    // handles the case of not finding a file
    if(number_of_locations == 0){
        std::cout << "file not found" << std::endl;
        return -1;
    }

    // data structure to store file location info
    recv(peerSocket, &file_length, sizeof(file_length), 0);
    file_size = file_length;
    int chunk_number = chunkNumber(file_length);

    for(int i=0; i<chunk_number; i++){
        temp_chunk.index = i;
        temp_chunk.is_possessed = false;
        chunks.push_back(temp_chunk);
    }

    // store the routing info into the client data structure
    for(int i=0; i<number_of_locations; i++){
        recv(peerSocket, &ip_address, sizeof(ip_address), 0);
        recv(peerSocket, &port, sizeof(port), 0);
        temp_address.s_addr = ip_address;

        recv(peerSocket, &number_of_chunks, sizeof(number_of_chunks), 0);

        for(int j=0; j<number_of_chunks; j++){
            recv(peerSocket, &chunk_index, sizeof(chunk_index), 0);

            for(int k=0; k<chunks.size(); k++){
                if(chunks[k].index == chunk_index){
                    temp_peer.address.s_addr = ip_address;
                    temp_peer.port = port;
                    chunks[k].peers.push_back(temp_peer);
                }
            }
        }
    }
    close(peerSocket);

    return 0;
}


// void Client::split(const std::string s, std::vector<std::string> &parameters, const char delim=' '){
//     parameters.clear();
//     std::istringstream iss(s);
//     std::string temp;

//     while(std::getline(iss, temp, delim)){
//         parameters.emplace_back(std::move(temp));
//     }

//     return;
// }


bool Client::fileExists(std::string file_name){
    struct stat buffer;
    return (stat(file_name.c_str(), &buffer) == 0);
}


int Client::downloadFile(std::string file_name){
    Client myClient;
    std::vector<chunk> chunks;
    std::vector<int> indexes;
    int file_length;

    requestFileLocation(file_name, chunks, file_length);

}
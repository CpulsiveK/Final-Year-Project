#ifndef PEERS_HPP
#define PEERS_HPP

#include <iostream>
#include <vector>
#include <string>
#include <strings.h>
#include <sstream>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <climits>
#include <unistd.h>
#include <arpa/inet.h>
#include <thread>
#include <mutex>

#define PORT 8082
#define CHUNK_SIZE 1024
#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8080

/*
    We need to define the basic structures that will be used in our
    program:
    * file_info will contain the filename and filesize
    * A peer will have an ip address and a port number to communicate on
    * A chunk will have an index to determine which peer's chunk, is_possessed and 
      a vector to store the peers
    * Finally a class to represent the client application which will hadnle all methods
*/

struct fileInfo {
    std::string file_name;
    uint32_t file_length;
};

struct peer {
    in_addr address;
    uint16_t port;
};

struct chunk {
    uint32_t index;
    bool is_possessed;
    std::vector<peer> peers;
};

class Client
{
    private:
        int chunkNumber(uint32_t file_length);
        int makeFilePublic(uint16_t number_of_files, std::vector<fileInfo> file_info);
        int requestFileAvailable();
        int requestFileLocation(std::string filename, std::vector<chunk> &chunks, int &file_size);
        bool fileExists(std::string filename);
        std::vector<int> downloadChunk(std::vector<chunk> chunks);
        int downloadChunkofFile(std::string filename, int index, struct chunk chunk_instance);
        int combine_file(std::string filename, int index);
        int downloadFile(std::string filename);
        long getFileSize(std::string filename);
        int parse_command(std::string command);
        void user_interface();
        void downloadRequestHandler(int process_fd, std::string filename, int chunk_index);
        void split(const std::string &s, std::vector<std::string> &parameters, const char delim);
        int writeLog(std::string filename, std::vector<chunk> chunks);
        int readLog(std::string filename, std::vector<std::string> &chunks, int &file_size);
    public:
        int execute(void);
};
#endif





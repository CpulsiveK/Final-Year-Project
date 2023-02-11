# Final-Year-Project

# SERVER
- Acknowledge files publicly made available by storing the file name, file length, which peer the file belongs to(ip address of peer)
- Keep track of the chunks needed for a specific file
- Acknowledge a search from a peer, ie when a peer searches for a file, the server should:
    Get the location(s) of the file (the ip address/addresses of the peer(s) with the file)
    Get the file length
    provide the chunks needed for the file 
- Provide list of files publicly available
- Should handle the above request from the peer

# PEERS
Should have a client application to handle:
- Make files publicly available
- Search for files
- Request a list of available files
- Keep track of the chunks needed for a specific file
- Download a file
- For every downloaded file we need to make it publicly available

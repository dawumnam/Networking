Dawum Nam
Networking Assignment 1 
TFTP 

1a connection, argparse, sending and receiving request, ack, data,
   terminating upon finishing file trasnfer or error, and file not found and
   file already exists error work. 

1b receiving host creates filename + 'new'  

2a TID checking and error does not work.(since TCP is connection based and 
   socket.recvfrom does not work, I couldnt find a way to check TID other than 
   modifyign and adding to extrea TID section to header)

2b timeout not implemented and tested

3 python3 server.py : starting server
  python3 python.py -i MustBeInserted -p 14599 -f nanpa
  
  Default is read and netascii. mode add -w for write mode -o for octet mode
  modify after -i , -p and -f as desire
  default port for server is 14599 and nanpa is included text file
  -i -p -f must be included
  



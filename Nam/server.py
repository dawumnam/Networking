import socket
import packet
import math
from functools import partial
import error
import os.path
#create socket bind host's ip and port and wait for connection
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print(ip)
port =14599
address = (ip,port)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(address)
server.listen(1)
print("Started listening on ",ip,":",port)
#upon receiving connection create new object called client
client,addr = server.accept()
print("Got a connection from ",addr[0],":",addr[1])
acceptedPort = addr[1]
#receiving request packet
recvd = client.recv(516)
#if error received close connection
if error.isPacketError(recvd) == True:
    client.close()
    exit()
#split opcode filename and mode into separate variables. 
opcode = int.from_bytes(recvd[0:2],byteorder='big')
fn_md = recvd[2:] 
fn_md = fn_md.split(b'\x00')
fn = fn_md[0].decode()
md = fn_md[1].decode()
#if read mode, check error and send data
if opcode == 1:
    if os.path.exists(fn) == False: 
        error.sendError(1,client)
        print('File Not Found, closing connection')
        client.close()
        exit()
    packet.send_data(fn,md,client)
    print('Transfer Successful!')
#if write, check error  and send ack with block number 0  
elif opcode == 2:
    if os.path.exists(fn+'new') == True: 
        error.sendError(6,client)
        print('File already exists, closing connection')
        client.close()
        exit()
    packet.send_ack(b'\x00\x00\x00\x00',client)
#receive data packet if received packet is error exit
    recvd = client.recv(516) 
    if error.isPacketError(recvd) == True:
        client.close()
        exit()
#if data is received open file and write accordingly
    if md == 'octet':
        f = open(fn+'new','wb')
    else:
        f = open(fn+'new','w')
    while True:
        data = recvd[4:]
        if md == 'octet':
            f.write(data)
        else:
            f.write(data.decode())
#if data is less than 512 bytes exit loop
        if len(data) < 512:
            f.close()
            print('Trnasfer successul!')
            break
#otherwise send ack and receive another data
        packet.send_ack(recvd[0:4],client)
        recvd = client.recv(516)
print('closing connection!')
client.close()
 



import argparse
import socket
import packet
from functools import partial
import error
import os.path

isWrite = False
isOctet = False
'''
Receiving Input
    -i Ip address - Required
    -p port number - required
    -f file name - required
    -w write mode by default it is read mode -w makes it write mode
    -o octet mode by default it is netascii mode -o makes it octet mode
'''
parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, dest='ip',help='Target Ip Address*REQUIRED*')
parser.add_argument('-p',required=True,type=int,dest='port',help='Target Port Number*REQUIRED*')
parser.add_argument('-f', required=True, dest='file',
        help = 'Enter file to be received or sent*REQUIRED*')
parser.add_argument('-w',action='store_true',dest='isWrite', help = 'Write to server DEFAULT:read')
parser.add_argument('-o',action='store_true',dest='isOctet', help = 'octet mode DEFAULT:netascii')
args = parser.parse_args()
'''
opcode set to 1 and mode set to 'netascii' by default 
if you pass either -w -o it changes value accordingly
'''
op = 1
mode = 'netascii'
if args.isWrite == True:
    op = 2
if args.isOctet == True:
    mode = 'octet'
#creates socket object and connect to target host
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = (args.ip,args.port)
client.connect(address)
#read mode initiated 
if op == 1:
    #if cannot create new file to put received data, close connection 
    #and send error packet
    if os.path.exists(args.file+'new') == True: 
        error.sendError(6,client)
        print('File already exists, closing connection')
        client.close()
        exit()
    #sending request
    packet.send_request(op,args.file,mode,client)
    recvd = client.recv(516)
    ''' if the data received after sending request is error packet
        saying that they dont have reqeusted file, close connection.
    '''
    if error.isPacketError(recvd) == True:
        client.close()
        exit()
    #if netascii mode write as 'w' and octet mode write as 'wb'
    if mode == 'octet':
        toWrite = open(args.file+'new','wb')
    else:
        toWrite = open(args.file+'new','w')
    #initiate endless while loop to receive data
    while True:
        data = recvd[4:]
        #split data from opcode and blocknumber
        #if octet mode write decoding
        if mode == 'octet':
            toWrite.write(data)
        #if netascii mode write with decoding
        else:
            toWrite.write(data.decode())
        #if data sent is less than 512, close connection
        if len(data) < 512:
            toWrite.close()
            print('Transfer successful')
            break
        #if data sent is equal to 512 send ack and receive another dasta
        packet.send_ack(recvd[0:4],client)
        recvd = client.recv(516)
#write mode, sending the data
elif op == 2:
    packet.send_request(op,args.file,mode,client)
    data = client.recv(516)
#receive ack, if error message received that they cannot create a file
#close connection.
    while True:
        if packet.isAckReceived(0,data) == True:
            break
        elif error.isPacketError(data) == True:
            client.close()
            exit()
#if file we want to send does not exist send error packet and exit connection
    if os.path.exists(args.file) == False: 
        error.sendError(1,client)
        print('File Not Found, closing connection')
        client.close()
        exit()
#otherwise send data
    packet.send_data(args.file,mode,client)
    print('Transfer successful!')
#close connection
print('Closing connection')
client.close()

    










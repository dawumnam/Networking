import socket
import time
from functools import partial
#checks if received packet is ack with correct blocknumber
#takes block number and packet return true or false
def isAckReceived(blockNumber,ackReceived):
    ackop = int.from_bytes(ackReceived[0:2],byteorder='big')
    ackbn = int.from_bytes(ackReceived[2:4],byteorder='big')
    if ackop == 4 and ackbn == blockNumber:
        return True
    else:
        return False
#send request if its read 01filename0mode0 is format
#if it is write, 02filename0mode0 is format
#takes opcode, file name mode and server to send packet
def send_request(rq, fn, md, server):
    message = bytearray()
    message.append(0)
    message.append(rq)
    fn = bytearray(fn.encode())
    message += fn
    message.append(0)
    mod = bytearray(md.encode())
    message += mod
    message.append(0)
    server.send(message)
#send ack to server, takes data to check blocknumber to be sent
#and server to send the ack packet
def send_ack(data,server):
    block = bytearray()
    block = data[2:4]
    message = bytearray()
    message.append(0)
    message.append(4)
    message += block
    server.send(message)
#send data to server
#takes filename and mode as an argument
def send_data(filename,mode,server):
#set mode accordingly
    md = 'r'
    if mode == 'octet':
        md = 'rb'
#open file as filename and mode
    with open(filename,md) as openfile:
#initial block number is 1
        block_number = 1
#as long as there's somethong left to be sent in a text file send
#every 512 bytes
        for dpacket in iter(partial(openfile.read,512),''):
            newdpacket = bytearray()
            newdpacket.append(0)
            newdpacket.append(3)
            newdpacket += block_number.to_bytes(2, byteorder='big')
            if md == 'r':
                newdpacket += dpacket.encode()
            elif md == 'rb':
                newdpacket += dpacket 
#upon sending data, if sent data is less than 516 close file and return
            server.send(newdpacket)
            if len(newdpacket) < 516:
                openfile.close()
                return
#otherwise wait for ack and increase block number by 1
            while True:
                ack = server.recv(4)
                if isAckReceived(block_number,ack) == True:
                    break
            block_number += 1 



    

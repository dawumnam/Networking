import argparse
import socket
import sys
from utils import Packet
from utils import States
import utils

parser = argparse.ArgumentParser()
parser.add_argument('-p',required=True,type=int,dest='port',help='Target Port Number*REQUIRED*')

args = parser.parse_args()
serversock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_address = ('localhost', args.port)
serversock.bind(server_address)
print('starting up on {} port {}'.format(*server_address))

class Server:
    def __init__(self):
        self.mode = ''
        self.fileName = ''
        self.state = States.closed
        self.recvdPacket = Packet()
        self.sentPacket = Packet()
        self.handshake()
      


    def handshake(self):
        while True:
            if self.state == States.closed:
                self.state = States.listen
                print("Server State: listening")
            elif self.state == States.listen:
                d,a = serversock.recvfrom(1472)
                self.recvdPacket.bitsToHeader(d)
                if self.recvdPacket.flag_urg == 1:
                    self.mode = 'r'
                else:
                    self.mode = 'w'
                self.fileName = d[104:].decode()
                print(self.fileName)
                print('Mode  = ',self.mode)
                if self.recvdPacket.flag_syn == 1:
                    self.state == States.synRcvd
                    self.sentPacket.randomSeq()
                    self.sentPacket.flag_ack = 1
                    self.sentPacket.flag_syn = 1
                    self.sentPacket.ack = self.recvdPacket.seq+1
                    header = self.sentPacket.bits()
                    serversock.sendto(header,a)
                    print("Server Received Syn, Server Sent Syn-Ack, Server State: Syn Received")
                    self.state = States.estab
            elif self.state == States.estab:
                d,a  = serversock.recvfrom(1472)
                self.recvdPacket.bitsToHeader(d)
                print("Connection Established")
                if self.recvdPacket.flag_ack == 1:
                    break

Server()
serversock.close()
                    

                    
                





        



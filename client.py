import socket
import sys
from utils import States
from utils import Packet
import utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, dest='ip',help='Target Ip Address*REQUIRED*')
parser.add_argument('-p',required=True,type=int,dest='port',help='Target Port Number*REQUIRED*')
parser.add_argument('-f', required=True, dest='file',
        help = 'Enter file to be received or sent*REQUIRED*')
args = parser.parse_args()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = (args.ip, args.port)


class Client:
    def __init__(self):
        self.mode = 'w'
        self.fileName = args.file
        self.state = States.closed
        self.recvdPacket = Packet()
        self.sentPacket = Packet()
        self.handshake()

    def handshake(self):
        while True:
            if self.state == States.closed:
                self.sentPacket.randomSeq()
                if self.mode == 'r':
                    self.sentPacket.flag_urg = 1
                else:
                    self.sentPacket.flag_urg = 0
                self.sentPacket.flag_syn = 1
                header = self.sentPacket.bits()
                header += self.fileName.encode()
                sock.sendto(header,server_address)
                self.state = States.synSent
                print("Syn sent to client, client State = SynSent")
            elif self.state == States.synSent:
                d,a = sock.recvfrom(1472)
                self.recvdPacket.bitsToHeader(d)
                if self.recvdPacket.flag_ack == 1 and self.recvdPacket.flag_syn == 1:
                    self.state = States.estab
                    self.sentPacket.clear()
                    self.sentPacket.seq = self.recvdPacket.ack
                    self.sentPacket.ack = self.recvdPacket.seq+1
                    self.sentPacket.flag_ack = 1
                    header = self.sentPacket.bits()
                    sock.sendto(header,a)
                    print('Received Syn-Ack and Sent Ack, Client State = established')
                else:
                    pass
            elif self.state == States.estab:
                break

Client()
sock.close()
                
                


        
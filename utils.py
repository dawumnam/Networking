import enum
import binascii
import random
import socket
import sys
import time
SMALLEST_STARTING_SEQ = 0
HIGHEST_STARTING_SEQ = 4294967295
DATA_DIVIDE_LENGTH = 1459
class States(enum.Enum):
    closed = 1
    listen = 2
    synSent = 3
    synRcvd = 4
    estab = 5
    finWaitOne = 6
    finWaitTwo = 7
    closeWait = 8
    closing = 9
    lasAck = 10
    timeWait = 11

class Packet:
    def __init__(self):
        self.seq = 0  # 32bit
        self.ack = 0  # 32bit
        self.flag_urg = 0  # 1bit
        self.flag_ack = 0  # 1bit
        self.flag_syn = 0  # 1bit
        self.flag_fin = 0  # 1bit
        self.window_size = 0  # 16bit
        self.checksum = 0  # 16bit
        self.data = 0
    
    def clear(self):
        self.seq = 0  # 32bit
        self.ack = 0  # 32bit
        self.flag_urg = 0  # 1bit
        self.flag_ack = 0  # 1bit
        self.flag_syn = 0  # 1bit
        self.flag_fin = 0  # 1bit
        self.window_size = 0  # 16bit
        self.checksum = 0  # 16bit
        self.data = 0
    
    def randomSeq(self):
        self.seq = random.randint(SMALLEST_STARTING_SEQ,HIGHEST_STARTING_SEQ)

    def bits(self):
        bits = '{0:032b}'.format(self.seq)
        bits += '{0:032b}'.format(self.ack)
        bits += '{0:01b}'.format(self.flag_urg)
        bits += '{0:01b}'.format(self.flag_ack)
        bits += '{0:01b}'.format(self.flag_syn)
        bits += '{0:01b}'.format(self.flag_fin)
        bits += '{0:016b}'.format(self.window_size)
        bits += '{0:016b}'.format(self.checksum)
        bits += '{0:04b}'.format(self.flag_urg)
        return bits.encode()
    
    def bitsToHeader(self,bit):
        bit = bit.decode()
        self.seq = int(bit[:32], 2)
        self.ack = int(bit[32:64], 2)
        self.flag_urg = int(bit[64], 2)
        self.flag_ack = int(bit[65], 2)
        self.flag_syn = int(bit[66], 2)
        self.flag_fin = int(bit[67], 2)
        self.window_size = int(bit[68:84], 2)
        self.checksum = int(bit[84:100], 2)

    def printEach(self):
        print('seq ',self.seq)
        print('ack ',self.ack)
        print(self.flag_urg,self.flag_ack,self.flag_syn,self.flag_fin)
        print('window ',self.window_size)
        print('checksum ',self.checksum)

def data_divider(data):
    """Divides the data into a list where each element's length is 1024"""
    data = [data[i:i + DATA_DIVIDE_LENGTH] for i in range(0, len(data), DATA_DIVIDE_LENGTH)]
    data.append("END")
    return data
'''
class Window:
    def __init__(self):
        self.windowSize = random.randint(3,10)
        self.retranWindow = list()
        self.sentUnacked = 0
        self.segmentAck = 0
        self.sendNext = 0

        self.recvNext = 0
        self.segmentSeq = 0
        self.recvUpperBound = self.recvNext+1459

    def checkValidAck(self, ack):
        if ack <= self.sendNext and ack > self.sentUnacked:
            return True
        else:
            return False
    def checkValidRecvd(self, recvd):
        if recvd >= self.recvNext and recvd < self.recvUpperBound:
            return True
        else:
            return False
    def insertToReTran(self, sent):
        if len(self.retranWindow < self.windowSize):
            self.retranWindow.append(sent)
        else:
            del(self.retranWindow[0])
            self.retranWindow.append(sent)  

    def reTransmit(self, server, sock):
        newList = self.retranWindow.reverse()
        for i in newList
            sock.sendto(i,server)

    def updateRecvWd(self, ackSent):
        self.recvNext = ackSent.ack
        self.recvUpperBound = self.recvNext + 1459

    def updateSendWd(self, sent):
        self.sentUnacked = sent.seq
        

    def recv(self,server,sock,fn):
        f = open(fn,'wb')
        endOfFile = False
        lastPacketRecived = time.time()
        starttime = time.time()
        while True:
            packet, addr = sock.recvfrom(1472)
            if len(packet[104:]) == 1459
'''

        

    




    



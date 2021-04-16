import packet


mode = {
        '0':'Not defined, see error message(if any).',
        '1':'File not found.',
        '2':'Access violation.',
        '3':'Disk full or allocation exceeded.',
        '4':'Illegal TFTP operation.',
        '5':'Unknown transfer ID.',
        '6':'File already exists.',
        '7':'No such user.'}
#check if packet is error receive data and return true or false
#if the data is error print error message 
def isPacketError(data):
    if int.from_bytes(data[:2],byteorder='big') == 5:
        errorMsg = mode[str(data[3])]
        print('Error received! closing connection!\n Error : '+errorMsg)
        return True
    else:
        return False
    
#function to send an error takes error code and server to send error packet 
def sendError(err,server):
    errorPacket = bytearray()
    errorPacket.append(0)
    errorPacket.append(5)
    errorPacket.append(0)
    if err == 0:
        errorPacket.append(0)
        errorMsg = mode['0'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 1:
        errorPacket.append(1)
        errorMsg = mode['1'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 2:
        errorPacket.append(2)
        errorMsg = mode['2'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 3:
        errorPacket.append(3)
        errorMsg = mode['3'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 4:
        errorPacket.append(4)
        errorMsg = mode['4'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 5:
        errorPacket.append(5)
        errorMsg = mode['5'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 6:
        errorPacket.append(6)
        errorMsg = mode['6'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    elif err == 7:
        errorPacket.append(7)
        errorMsg = mode['7'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)
    else:
        errorPacket.append(0)
        errorMsg = mode['0'].encode()
        errorPacket += errorMsg
        errorPacket.append(0)
        server.send(errorPacket)


        
        
     
   
        
        
     
        
        
        
        


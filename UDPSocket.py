import socket
import threading
import Resolution

def serverUdp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    PORT = 9090

    network = '<broadcast>'
    s.sendto('GETIP\r\n'.encode('utf-8'), (network,PORT))

    while True:
        data, address = s.recvfrom(9090)
        snid = data.decode('utf-8').split('\r\n')[1].split(':')[1]
        reverseSnid = snid[::-1]
        readySnid = ''
        i = 0
        while(i<=6):
            readySnid = readySnid + reverseSnid[i:i+2][::-1]
            i += 2
            
        print(readySnid)
        print('snid{}:{}'.format(address, data.decode('utf-8').split('\r\n')[1]))
        tcpThread = TCPThread(address, readySnid)
        tcpThread.start()
        
def clientTcp(address, readySnid):
    port = 8001
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ip = address[0]
    client.connect((ip, port))
    snid = "0800" + readySnid + "fe9d"
    bytes = bytearray.fromhex(snid)
    client.send(bytes)
    print(bytes)
    while True:
        data = client.recvfrom(1024*1024)
        deviceBytes = data[0]
        
        if(data!=None):
            print(deviceBytes.hex())
            Resolution.resolution(deviceBytes.hex())
            continue
        
class TCPThread(threading.Thread):
    def __init__(self, address, readySnid):
        threading.Thread.__init__(self)
        self.address = address
        self.readySnid = readySnid
        
    def run(self):
        clientTcp(self.address, self.readySnid)

#serverUdp()

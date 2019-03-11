import threading
import UDPSocket


class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
     
    def run(self):
        print("start")
        UDPSocket.serverUdp()


thread = myThread("newUDPThread")
thread.start()


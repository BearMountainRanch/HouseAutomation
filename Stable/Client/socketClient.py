# socketClient.py
import socket
# import config
from time import sleep

class Client():

    HOST = "10.0.0.33"
    PORT = 50007
    SOCKET_NAME = "PumpSensor"
    BUFSIZE = 1024

    def __init__(self) -> None:
        self.connect()
        # self.state = config.state
        # self.states = config.states

    def connect(self) -> None:
        '''Connect to host server through port'''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.send(self.SOCKET_NAME)
        sleep(1) # Waiting for Server to record Client Name before continuing

    def close(self) -> None:
        self.s.close()

    def isConnected(self) -> bool:
        '''Checks connection to Server and connects if not'''
        try:
            self.s.send(b"-")
            return True
        except:
            self.close()
            self.connect()
            return False

    # WORKING ON THIS
    def send(self, msg) -> bool:
        '''Send msg to Server and check full msg was sent'''
        try:
            byte = self.s.send(msg.encode('ascii'))
            print("BYTE: ", byte)
        except:
            # Server is down
            # self.state = self.states[1]
            return False
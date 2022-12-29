# socketClient.py
import socket

class Client:

    HOST = "192.168.0.2" # BMR Server
    PORT = 0
    BUFSIZE = 1024

    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self) -> bool:
        '''Connect to host server through port'''
        try:
            self.s.connect((self.HOST, self.PORT))
            return True
        except TimeoutError:
            return False 
        except InterruptedError:
            return False

    def send(self, package) -> bool:
        '''Send package if connection exists'''
        package = str(package)
        cksum = self.checksum(package)
        try:
            self.s.send(package)
            if self.s.recv(self.BUFSIZE) != cksum:
                self.send(package)
            return True
        except:
            con = False
            while not con:
                con = self.connect()
            self.send(package)

    def checksum(self, package:list[str]) -> str:
        '''Create a checksum for package'''
        checksum = 0
        for i in package:
            for j in i:
                checksum = checksum ^ ord(j)
        return str(checksum)[-2:]
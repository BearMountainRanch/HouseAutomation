# socketClient.py
import socket

class Server():

    HOST = "" # BMR Server
    PORT = 50007
    BUFSIZE = 1024

    def __init__(self) -> None:
        self.clients = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)
        self.accept()

    def accept(self) -> None:
        '''Connect to host server through port'''
        conn, addr = self.s.accept()
        print('Connected by', addr)
        self.clients.append(conn)

    def send(self, package) -> bool:
        '''Send package if connection exists'''
        package = str(package)
        cksum = self.checksum(package)

        self.clients[0].sendall(package)
        print("Sent: ", package)

        # try:
        #     self.s.sendall(package)
        #     if self.s.recv(self.BUFSIZE) != cksum:
        #         self.send(package)
        #     return True
        # except:
        #     con = False
        #     while not con:
        #         con = self.connect()
        #     self.send(package)
    
    def recieve(self) -> str:
        msg = self.s.recv()
        print("Recv: ", msg)
        return msg

    def checksum(self, package:list[str]) -> str:
        '''Create a checksum for package'''
        checksum = 0
        for i in package:
            for j in i:
                checksum = checksum ^ ord(j)
        return str(checksum)[-2:]
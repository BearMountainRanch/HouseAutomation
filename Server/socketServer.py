# socketServer.py
import socket
from time import sleep

class Server():

    HOST = ""
    PORT = 50007
    BUFFSIZE = 1024

    def __init__(self) -> None:
        self.clients = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        self.s.settimeout(0)

    def accept(self) -> None:
        '''Connect to host server through port'''
        try:
            conn, addr = self.s.accept()
            sleep(.5) # Give client time to conenct and send Name
            clientName = self.recieve(conn)
            self.clients[clientName] = conn
            print('Connected by', addr)
        except OSError:
            pass

    def isConnected(self) -> bool:
        '''Update list of connected clients to server'''
        for client in self.clients:
            try:
                self.clients[client].send(b"-")
                return True
            except:
                del self.clients[client]
                return False

    def recieve(self, client) -> str:
        '''Recieve msg from given client and reuturn msg or None'''
        try:
            return client.recv(self.BUFFSIZE).decode('ascii')
        except:
            return None
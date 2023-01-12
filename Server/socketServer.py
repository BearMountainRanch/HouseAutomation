# socketServer.py
import socket
import config
import time

class Server():

    HOST = ""
    PORT = 50007

    def __init__(self) -> None:
        self.clients = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        self.s.settimeout(0)

    def accept(self) -> None:
        '''Connect to host server through port'''
        try:
            # time.sleep(.5)
            conn, addr = self.s.accept()
            self.clients.append(Client(conn, addr))
            # Loop until name is recieved
            clientName = ""
            while clientName == "":
                clientName = self.clients[-1].recieve()
            self.clients[-1].setName(clientName)

            print("Accepting {} as IP:{}".format(clientName, addr))
        except OSError:
            pass

    def isConnected(self) -> None:
        '''Update list of connected clients to server'''
        for client in self.clients:
            # if self.send(client.conn, ""):
            if client.send(""):
                pass
            else:
                self.clients.remove(client)
                break


class Client():

    def __init__(self, conn, addr) -> None:
        '''Constructor to initilize client'''
        self.conn = conn
        self.addr = addr

    def setName(self, name) -> None:
        '''Sets the name of the object'''
        self.name = name

    def recieve(self) -> str:
        '''Recieve msg from given client and reuturn msg or None'''

        try:
            # Wait for buffer to have a value
            start = time.time()
            while not config.timeout(start, 1):
                val = self.conn.recv(1)
                if val == None:
                    continue
                else:
                    break

            # # Enter if timeout was reached
            if config.timeout(start, 1):
                # self.logs.warning(self.LOC, "Read Timeout")
                return ""

            # Look for starting frame
            collectData = False
            if val == b"{":
                collectData = True
            else:
                # Starting frame expected and was not recieved
                # self.logs.warning(self.LOC, "Data message corupted from beggining: {}".format(val))
                return self.recieve()

            # Start to build message
            msg = ""
            while collectData:
                byte = self.conn.recv(1).decode('ascii')
                if byte == "}":
                    collectData = False
                elif byte == "{":
                    # self.logs.error(self.LOC, "Data message corupted during")
                    msg = ""
                else:
                    msg += byte
        
            return msg
            
        except:
            # self.logs.error(self.LOC, "Sensor Read Intrupt")
            return ""

    def send(self, msg:str) -> bool:
        '''Send msg to Client and check full msg was sent'''
        try:
            msgBytes = 0
            msg = "{" + msg + "}"
            while msgBytes != len(msg):
                msgBytes = self.conn.send(msg.encode('ascii'))
            return True
        except:
            # Client no longer exists
            return False
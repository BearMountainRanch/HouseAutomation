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
        '''Connect to Client through port'''
        try:
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
            if client.send(""):
                pass
            else:
                print("Removing {} as a Client".format(client.name))
                self.clients.remove(client)
                break

    def close(self) -> None:
        '''Close Socket (if it does not exist just pass)'''
        try:
            self.s.close()
        except:
            pass

class Client():

    def __init__(self, conn, addr) -> None:
        '''Constructor to initilize client'''
        self.conn = conn
        self.addr = addr
        self.recvBuffer = ""

    def setName(self, name) -> None:
        '''Sets the name of the object'''
        self.name = name

    def recv(self) -> None:
        '''Transfer machine buffer to program buffer'''
        try:
            self.recvBuffer += self.conn.recv(1024).decode('ascii').replace("{}", "")
            print("BUF: ", self.recvBuffer)
        except OSError as e:
            print("RECV: ", e)

    def getRecvBuf(self, buf:int) -> str:
        '''Return msg that is buf long'''
        try:
            msg = self.recvBuffer[:buf]
            self.recvBuffer = self.recvBuffer[buf:]
            return msg
        except:
            return ""

    def recieve(self) -> str:
        '''Recieve msg from given client and reuturn msg or None'''
        self.recv()
        try:
            val = self.getRecvBuf(1)

            # Look for starting frame
            collectData = False
            if val == "{":
                collectData = True
            else:
                # Starting frame expected and was not recieved
                return ""

            # Start to build message
            msg = ""
            while collectData:
                byte = self.getRecvBuf(1)
                if byte == "}":
                    collectData = False
                elif byte == "{":
                    msg = ""
                else:
                    msg += byte

            print("MSG: ", msg)
            return msg
            
        except OSError as e:
            print(e)
            # self.logs.error(self.LOC, "Sensor Read Intrupt")
            return ""

    def send(self, msg:str) -> bool:
        '''Send msg to Client and check full msg was sent'''
        try:
            msg = "{" + msg + "}"
            self.conn.send(msg.encode('ascii'))
            return True
        except OSError as e:
            print(e)
            # Client no longer exists
            return False
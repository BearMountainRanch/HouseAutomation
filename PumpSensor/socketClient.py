# socketClient.py
import socket
import config
import time

class Client():

    HOST = "10.0.0.33"
    PORT = 50007
    SOCKET_NAME = "Pump"

    def __init__(self) -> None:
        self.connect()
        self.state = config.state
        self.states = config.states
        self.s.settimeout(.1)
        self.recvBuffer = ""

    def connect(self) -> None:
        '''Connect to host server through port'''
        while True:
            try:
                time.sleep(1) # (Important) Gives time on unexpected shutdown
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.HOST, self.PORT))
                self.send(self.SOCKET_NAME)
                time.sleep(1) # (Important) Gives time on unexpected shutdown
                break
            except OSError as e:
                print("CON: ", e)
                self.close()
                continue

    def close(self) -> None:
        '''Close Socket (if it does not exist just pass)'''
        try:
            self.s.close()
        except OSError as e:
            print("CLOSE: ", e)

    def isConnected(self) -> bool:
        '''Checks connection to Server and connects if not'''
        if self.send(""):
            print("T")
            return True
        else:
            print("F")
            self.reConnect()
            return False

    def reConnect(self) -> None:
        '''Reconnect to socket'''
        self.close()
        self.connect()

    def recv(self) -> None:
        '''Transfer machine buffer to program buffer'''
        try:
            self.recvBuffer += self.s.recv(1024).decode('ascii').replace("{}", "")
            print("BUF: ", self.recvBuffer)
        except:
            pass

    def getRecvBuf(self, buf:int) -> str:
        '''Return msg that is buf long'''
        try:
            msg = self.recvBuffer[:buf]
            self.recvBuffer = self.recvBuffer[buf:]
            return msg
        except:
            return ""

    def recieve(self) -> str:
        '''Recieve msg from Server and reuturn msg or None'''
        self.recv()
        try:
            val = self.getRecvBuf(1)

            # Look for starting frame
            collectData = False
            if val == b"{":
                collectData = True
            else:
                # Starting frame expected and was not recieved
                print("Nothing here")
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

            return msg
            
        except OSError as e:
            print(e)
            return ""

    def send(self, msg:str) -> bool:
        '''Send msg to Server and check full msg was sent'''
        try:
            msg = "{" + msg + "}"
            self.s.send(msg.encode('ascii'))
            # time.sleep(.1) # Give time for msg to send
            return True
        except OSError as e:
            print("SEND: ", e)
            # Server is down
            self.state = self.states[1]
            # self.reConnect()
            return False
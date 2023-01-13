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
        self.s.settimeout(0)

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
            except OSError:
                self.close()
                continue

    def close(self) -> None:
        '''Close Socket (if it does not exist just pass)'''
        try:
            self.s.close()
        except:
            pass

    def isConnected(self) -> bool:
        '''Checks connection to Server and connects if not'''
        if self.send(""):
            return True
        else:
            self.reConnect()
            return False

    def reConnect(self) -> None:
        '''Reconnect to socket'''
        self.close()
        self.connect()

    def recieve(self) -> str:
        '''Recieve msg from Server and reuturn msg or None'''
        try:
            # Wait for buffer to have a value
            start = time.time()
            while not config.timeout(start, 1):
                print(".")
                val = self.s.recv(1) # Stops being able to recieve data here and failes
                print("-")
                if val == None:
                    continue
                else:
                    break

            # Look for starting frame
            collectData = False
            if val == b"{":
                collectData = True
            else:
                # Starting frame expected and was not recieved
                print("Start Frame")
                return self.recieve()

            # Start to build message
            msg = ""
            while collectData:
                byte = self.s.recv(1).decode('ascii')
                if byte == "}":
                    collectData = False
                elif byte == "{":
                    msg = ""
                else:
                    msg += byte

            return msg
            
        except:
            return ""

    def send(self, msg:str) -> bool:
        '''Send msg to Server and check full msg was sent'''
        try:
            msgBytes = 0
            msg = "{" + msg + "}"
            while msgBytes != len(msg):
                msgBytes = self.s.send(msg.encode('ascii'))
            time.sleep(.1) # Give time for msg to send
            return True
        except:
            # Server is down
            self.state = self.states[1]
            # self.reConnect()
            return False
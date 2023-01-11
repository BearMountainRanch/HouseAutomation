# socketServer.py
import socket
import config
import time

class Server():

    HOST = ""
    PORT = 50007

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
            # Should be able to remove this line with new protocal
            time.sleep(.5) # Give client time to conenct and send Name
            clientName = self.recieve(conn)
            self.clients[clientName] = conn
            print('Connected by', addr)
        except OSError:
            pass

    def isConnected(self) -> bool:
        '''Update list of connected clients to server'''
        for client in self.clients:
            try:
                self.send(self.clients[client], "{}")
                return True
            except:
                del self.clients[client]
                return False

    def recieve(self, client:socket) -> str:
        '''Recieve msg from given client and reuturn msg or None'''

        try:
            # Wait for buffer to have a value
            start = time.time()
            while not config.timeout(start, 1):
                val = client.recv(1)
                if val == None:
                    continue
                else:
                    break

            # # Enter if timeout was reached
            # if config.timeout(start, 1):
            #     self.logs.warning(self.LOC, "Read Timeout")
            #     return ''

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
                byte = client.recv(1).decode('ascii')
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

    def send(self, client:socket, msg:str) -> bool:
        '''Send msg to Client and check full msg was sent'''
        try:
            msgBytes = 0
            msg = "{" + msg + "}"
            while msgBytes != len(msg):
                msgBytes = client.send(msg.encode('ascii'))
            return True
        except:
            # Client no longer exists
            return False
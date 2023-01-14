# Main.py
import _thread
from socketServer import Server
import config
import time

class Main():

    def __init__(self) -> None:
        self.srv = Server()
        self.sendBuffer = [] # tuple(clientName, msg)
        self.recvBuffer = []

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            time.sleep(10) # To keep debugging sane and reasonable
            self.sendBuffer.append(("Pump", config.msgs[0]))
            time.sleep(10) # To keep debugging sane and reasonable
            self.sendBuffer.append(("Pump", config.msgs[1]))

    def socket(self) -> None:
        '''Main Socket Loop in Core1'''
        while True:

            time.sleep(.3) # Allows the Pico to keep up
            # Check connection to Clients
            self.srv.accept()
            self.srv.isConnected()

            # try:
            #     self.srv.s.recv(1024)
            # except:
            #     pass

            # Send msgs from sendBuffer to desigated clients
            sendBuffer = self.sendBuffer
            for packet in sendBuffer:
                for client in self.srv.clients:
                    if packet[0] == client.name:
                        client.send(packet[1]) # Send data
                        self.sendBuffer.remove(packet)
                        break

            # Recv data into the recvBuffer
            for client in self.srv.clients:
                msg = client.recieve()
                if msg == None:
                    continue
                self.recvBuffer.append(msg)

if __name__ == "__main__":
    try:
        main = Main()
        _thread.start_new_thread(main.socket, ())
        main.loop()
    except KeyboardInterrupt:
        main.srv.close()
        print("Socket closed succesfully")
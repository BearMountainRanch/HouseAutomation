# Main.py
import _thread
from socketServer import Server
from time import sleep

class Main():

    def __init__(self) -> None:
        self.srv = Server()
        self.sendBuffer = []
        self.recvBuffer = []

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            pass

    def socket(self) -> None:
        '''Main Socket Loop in Core1'''
        while True:
            sleep(1) # To keep debugging sane and reasonable

            # Check connection to Clients
            self.srv.accept()
            self.srv.isConnected()
            print("Clients: ", self.srv.clients)

            # Somehow send msgs from a buffer to desigated clients
            # Logic

            # Recv data into the recvBuffer
            self.recvBuffer.append(self.srv.recieve())

if __name__ == "__main__":
    main = Main()
    _thread.start_new_thread(main.socket)
    main.loop()
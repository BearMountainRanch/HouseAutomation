# Main.py
from socketServer import Server
from time import sleep

class Main():

    def __init__(self) -> None:
        self.srv = Server()

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            self.srv.accept()
            self.srv.isConnected()
            print("Clients: ", self.srv.clients)
            sleep(1) # To keep debugging sane and reasonable

if __name__ == "__main__":
    run = Main()
    run.loop()
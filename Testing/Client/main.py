# Main.py
import _thread
from socketClient import Client
from time import sleep

class Main():

    LED_PIN = "LED"
    WIFI_FILE_NAME = "wifi.txt"

    def __init__(self) -> None:
        self.cli = Client()
        self.sendBuffer = []
        self.recvBuffer = []

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            
            sleep(1)

    def socket(self) -> None:
        '''Main Socket Loop in Core1'''
        while True:

            # Check connection to Server
            self.cli.isConnected()

            try:
                self.cli.s.recv(1024)
            except:
                pass


if __name__ == "__main__":
    main = Main()
    _thread.start_new_thread(main.socket, ())
    main.loop()
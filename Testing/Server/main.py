# Main.py
import network
from time import sleep
from machine import Pin
from socketServer import Server

class State():

    LED_PIN = "LED"
    SSID = 'UCSDFellas'
    PWD = '420BlazeIt'

    def __init__(self) -> None:
        self.connect()
        self.LED = Pin(self.LED_PIN, Pin.OUT)

    def lightToggle(self, data) -> None:
        self.LED.value(data)

    def loop(self) -> None:
        '''Main program loop'''
        cnt = 0
        state = 0
        while cnt < 100:
            server.accept()
            print(server.clients)
            if not server.clients:
                print('No clinets')
                sleep(1)
                continue
            for client in server.clients:
                with client:
                    while True:
                        data = client.recv(1024)
                        data = repr(data)
                        if data == 'None':
                            break
                        elif data == '1':
                            data = True
                        elif data == '0':
                            data = False
                        self.lightToggle(data)
            
            if state == 0:
                server.send(b'1')
                state = 1
            else:
                server.send(b'0')
            sleep(1)
            cnt = cnt + 1

    def connect(self) -> None:
        '''Connect to WLAN'''
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.SSID, self.PWD)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        print(wlan.ifconfig())


if __name__ == "__main__":
    run = State()
    server = Server()
    run.loop()
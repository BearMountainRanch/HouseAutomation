# Main.py
import network
from time import sleep
from machine import Pin
from socketClient import Client

class State():

    LED_PIN = "LED"
    SSID = 'UCSDFellas'
    PWD = '420BlazeIt'

    def __init__(self) -> None:
        self.connect()
        self.ledState = False
        self.LED = Pin(self.LED_PIN, Pin.OUT)
        
    def lightToggle(self, data) -> None:
        self.LED.value(data)

    def loop(self) -> None:
        '''Main program loop'''
        cnt = 0
        state = False
        data = 0
        while cnt < 100:
            state = client.recieve()
            if state == None:
                continue
            elif state == 1:
                state = True
            elif state == 0:
                state = False
            cnt = cnt + 1
            self.lightToggle(state)

            if cnt % 10 == 0:
                if data == 0:
                    client.send(b'1')
                    data = 1
                elif data == 1:
                    client.send(b'0')
                    data = 0

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
    client = Client()
    run.loop()
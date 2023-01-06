# Main.py
import network
from time import sleep
from machine import Pin
from socketClient import Client

class State():

    LED_PIN = 25
    SSID = 'Home'
    PWD = '9512783540'

    def __init__(self) -> None:
        self.connect()
        self.ledState = False
        self.LED = Pin(self.LED_PIN, Pin.OUT)
        
    def lightToggle(self) -> None:
        if self.ledState:
            self.LED.value(False)
            self.ledState = False
        else:
            self.LED.value(True)
            self.ledState = True

    def loop(self) -> None:
        '''Main program loop'''
        cnt = 0
        state = False
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
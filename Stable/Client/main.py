# Main.py
import network
from machine import Pin
from time import sleep
from socketClient import Client
# import config

class Main():

    LED_PIN = "LED"
    WIFI_FILE_NAME = "wifi.txt"

    def __init__(self) -> None:
        self.connect()
        self.led = Pin(self.LED_PIN, Pin.OUT)
        self.led.on()
        self.cli = Client()

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            sleep(1) # To keep debugging sane and reasonable
            self.cli.isConnected()

    def connect(self) -> None:
        '''Connect to WLAN'''
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        SSID, PWD = self.wifiFileRead()
        wlan.connect(SSID, PWD)
        while wlan.isconnected() == False:
            pass
        print("WLAN: ", wlan.ifconfig())

    def wifiFileRead(self) -> tuple[str, str]:
        '''Read Wifi file and return SSID and Password'''
        with open(self.WIFI_FILE_NAME, 'r') as wifi:
            SSID, PWD = wifi.read().split("\r\n")
        return SSID, PWD

    def wifiFileWrite(self, SSID, PWD) -> bool:
        '''Write Wifi file and return True if succesful'''
        try:
            with open(self.WIFI_FILE_NAME, 'w') as wifi:
                wifi.write("{}\n{}".format(SSID, PWD))
            return True
        except:
            return False

if __name__ == "__main__":
    run = Main()
    run.loop()
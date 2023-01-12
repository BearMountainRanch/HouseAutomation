# Main.py
import network
from machine import Pin
from time import sleep
import _thread
from socketClient import Client
import config

class Main():

    LED_PIN = "LED"
    WIFI_FILE_NAME = "wifi.txt"

    def __init__(self) -> None:
        self.connect()
        self.led = Pin(self.LED_PIN, Pin.OUT)
        self.led.on()
        self.cli = Client()
        self.sendBuffer = []
        self.recvBuffer = []

    def loop(self) -> None:
        '''Main program loop'''
        while True:
            sleep(1) # To keep debugging sane and reasonable
            
            recvBuffer = self.recvBuffer
            # print("Buff: ", recvBuffer)
            for msg in recvBuffer:
                if msg == config.msgs[0]:
                    self.led.on()
                    self.recvBuffer.remove(msg)
                elif msg == config.msgs[1]:
                    self.led.off()
                    self.recvBuffer.remove(msg)
                else:
                    # Msg recvied does not match protocall
                    pass

    def socket(self) -> None:
        '''Main Socket Loop in Core1'''
        while True:
            sleep(1) # To keep debugging sane and reasonable

            # Check connection to Server
            self.cli.isConnected()

            # Send data in the sendBuffer and clear msg from sendBuffer 
            sendBuffer = self.sendBuffer
            for msg in sendBuffer:
                self.cli.send(msg)
                self.sendBuffer.remove(msg)

            # Recv data into the recvBuffer
            msg = self.cli.recieve()
            if len(msg) != 0:
                self.recvBuffer.append(msg)


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

    def wifiFileWrite(self, SSID:str, PWD:str) -> bool:
        '''Write Wifi file and return True if succesful'''
        try:
            with open(self.WIFI_FILE_NAME, 'w') as wifi:
                wifi.write("{}\n{}".format(SSID, PWD))
            return True
        except:
            return False

if __name__ == "__main__":
    main = Main()
    _thread.start_new_thread(main.socket, ())
    main.loop()
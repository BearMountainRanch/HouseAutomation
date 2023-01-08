from machine import Pin
import _thread
from time import sleep

led = Pin("LED", Pin.OUT)
end = 0

def CoreTask(len):
    global end
    for i in range(len):
        print("Second Thred: {}".format(i))
        end = i
        sleep(4)
        
_thread.start_new_thread(CoreTask, (10))

while end < 10:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
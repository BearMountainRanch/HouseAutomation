# config.py
import time

# Standard Message Protocall (Same for Server)
msgs = ["LED1", "LED2"]

def timeout(start:float, duration:int) -> bool:
    '''Determines if a timeout was reached | Returns bool'''
    if (time.time() - start) > duration:
        return True
    else:
        return False
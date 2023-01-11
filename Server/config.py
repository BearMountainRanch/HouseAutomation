# config.py
import time

def timeout(start:float, duration:int) -> bool:
    '''Determines if a timeout was reached | Returns bool'''
    if (time.time() - start) > duration:
        return True
    else:
        return False
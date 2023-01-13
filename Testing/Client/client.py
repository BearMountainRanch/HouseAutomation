# echo-client.py

import socket
from time import sleep

HOST = "10.0.0.33"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0)
    
while True:
    try:
        data = s.recv(1).decode('ascii')
        if not data:
            break
        print(f"Received {data}")
    except:
        sleep(.1)
        print(".")
        pass


print("DONE")
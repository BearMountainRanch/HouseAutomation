# echo-server.py

import socket
import time

HOST = ""
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()


for i in range(10):
    time.sleep(1)
    conn.send(str(i).encode('ascii'))

time.sleep(2)
#!/usr/bin/env python3
import socket

HOST = ''       # The server's hostname or IP address
PORT = 8080     # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        tosend = input("")
        s.sendall(bytes(tosend, "utf-8"))
        data = s.recv(1024)
        print(f"Received {repr(data)}")

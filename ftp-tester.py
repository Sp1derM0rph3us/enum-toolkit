#!/usr/bin/python3

import socket, sys

p = int(sys.argv[2])
target = str(sys.argv[1])
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((target,p))

banner = tcp.recv(1024).decode('utf-8').strip()
print(banner)

auth = "USER ftp\r\n"
passw = "PASS ftp\r\n"

print(auth)
tcp.sendall(auth.encode('utf-8'))
user = tcp.recv(1024).decode('utf-8').strip()
print(user)
print(passw)
tcp.sendall(passw.encode('utf-8'))
passr = tcp.recv(1024).decode('utf-8').strip()
print(passr)
print("HELP\r\n")
tcp.sendall("HELP".encode('utf-8'))
hr = tcp.recv(1024).decode('utf-8').strip()
print(hr)
tcp.close()


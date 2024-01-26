#!/usr/bin/python3

import socket,sys,time


if len(sys.argv) != 3:
    print("Usage: ./ftp-tester.py [target] [port]")

else:
    p = int(sys.argv[2])
    target = str(sys.argv[1])
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((target,p))

    banner = tcp.recv(1024).decode('utf-8').strip()
    print(banner)

    auth = "USER ftp\r\n"
    passw = "PASS ftp\r\n"

    print(auth)
    tcp.send(auth.encode('utf-8'))
    user = tcp.recv(1024).decode('utf-8').strip()
    print(user)
    time.sleep(0.5)
    print(passw)
    tcp.send(passw.encode('utf-8'))
    passr = tcp.recv(1024).decode('utf-8').strip()
    print(passr)
    time.sleep(0.5)
    lresp = tcp.recv(1024).decode('utf-8').strip()
    print(lresp)
    if passr.startswith("230"):
        print("[!] FTP:FTP Login is valid!")
        tcp.close()
    else:
        print("[-] FTP:FTP Login is invalid :(")
        tcp.close()


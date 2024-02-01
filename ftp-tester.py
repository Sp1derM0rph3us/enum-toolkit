#!/usr/bin/python3
# Simple FTP auth tester. Passing only target and port it will try to log in with ftp:ftp credentials
# Passing user and passwordlist will try to perform a brute force.
# Made by: Sp1d3rM0rph3us
# WORK IN PROGRESS BTW

import socket,sys,time


if len(sys.argv) > 5 or len(sys.argv) < 3 :
    print("Usage: ./ftp-tester.py [target] [port] [userlist] [passlist]")

else:
    p = int(sys.argv[2])
    target = str(sys.argv[1])


    if len(sys.argv) == 3:

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

    else:

        auth = []
        passw = []
        with open(sys.argv[3], "r") as file:
            for l in file:
                auth.append(l.strip())

        with open(sys.argv[4], "r") as file:
            for l in file:
                passw.append(l.strip())

        print("[*] Starting brute force...")
        for user in auth:
            for passwd in passw:

                print(f"[*] Attempting {user}:{passwd}")
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect((target,p))
                banner = tcp.recv(1024).decode('utf-8').strip()
                tcp.send(f"USER {user}\r\n".encode('utf-8'))
                tcp.recv(1024).decode('utf-8').strip()
                tcp.send(f"PASS {passwd}\r\n".encode('utf-8'))
                passr = tcp.recv(1024).decode('utf-8').strip()
                if passr.startswith("230"):
                    print(f"[!] Credentials found: {user}:{passwd}")
                    tcp.send("BYE\r\n".encode('utf-8'))
                tcp.close()
                time.sleep(0.5)

#!/usr/bin/python3
# Simple banner grabber in python
# Made by: Sp1d3rM0rph3us

import socket, sys, ssl

common_http_ports = [80, 8080, 10000]
common_https_ports = [443, 8443]

def http_banner_graber(target, p):
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, p))
        request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\n\r\n"
        tcp.send(request.encode())
        
        # Retrieving the banner
        banner = tcp.recv(1024).decode('utf-8').strip()
        print(banner)
    except Exception as e:
        print("Error: ", e)
    finally:
        tcp.close()

def https_banner_graber(target, p):
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, p))
        
        # Adding SSL/TLS layer to the connection
        context = ssl.create_default_context()
        ssl_socket = context.wrap_socket(tcp, server_hostname=target)

        # Sending the request
        request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\n\r\n"
        ssl_socket.send(request.encode())

        # Retrieving the banner
        banner = ssl_socket.recv(1024).decode('utf-8').strip()
        print(banner)
    except Exception as e:
        print("Error: ", e)
    finally:
        if ssl_socket:
            ssl_socket.close()

def banner_graber(target, p):
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, p))
        
        banner = tcp.recv(1024).decode('utf-8').strip()
        print(banner)
    except Exception as e:
            print("Error: ", e)
    finally:
        tcp.close()


## Checking if arguments were given ##

if len(sys.argv) != 3:
    print("""Usage: ./bgrabber.py [target] [port]
Usage 2: py3 bgrabber.py [target] [port]""")

else:
    target = str(sys.argv[1])
    p = int(sys.argv[2])
    
    if p in common_http_ports:
        print(f"[+] Banner for {target}:{p}")
        http_banner_graber(target, p)

    elif p in common_https_ports:
        print(f"[+] Banner for {target}:{p}")
        https_banner_graber(target, p)
    else:
        print(f"[+] Banner for {target}:{p}")
        banner_graber(target,p)

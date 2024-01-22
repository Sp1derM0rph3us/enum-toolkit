#!/usr/bin/python3
# Simple banner grabber in python
# Made by: Sp1d3rM0rph3us

import socket, sys, ssl, time, re

common_http_ports = [80, 8080, 10000]
common_https_ports = [443, 8443]

def http_banner_graber(target, p):
    tcp = None
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
        if tcp:
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

def smtp_banner_grabber(target, p):
    tcp = None
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, p))
        time.sleep(1.5)
        banner = tcp.recv(1024).decode('utf-8').strip()
        print(banner)

        # Creating the request
        with open(sys.argv[3], 'r') as wordlist:
            user_list = wordlist.read().splitlines()

        for user in user_list:
            request = f"VRFY {user}\r\n"
            tcp.send(request.encode())
            response = tcp.recv(1024).decode('utf-8').strip()
            fresponse = response.rsplit(maxsplit=1)
            time.sleep(0.5)
            if re.search("252", response):
                if len(fresponse) > 1:
                    print(f"[+] USER FOUND: {fresponse[1]}")
                else:
                    print(f"[+] USER FOUND: {response}")

    except Exception as e:
        print("Error: ", e)

    finally:
        if tcp:
            tcp.close()


def banner_graber(target, p):
    tcp = None
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, p))
        
        banner = tcp.recv(1024).decode('utf-8').strip()
        print(banner)
    except Exception as e:
            print("Error: ", e)
    finally:
        if tcp:
            tcp.close()


## Checking if arguments were given ##

if len(sys.argv) < 3:
    print("""Usage: ./bgrabber.py [target] [port]
Usage 2: py3 bgrabber.py [target] [port]

If you want to bruteforce users in smtp, add the path to your usernames wordlist as the last argument""")

else:
    target = str(sys.argv[1])
    p = int(sys.argv[2])
    
    if p in common_http_ports:
        print(f"[+] Banner for {target}:{p}")
        http_banner_graber(target, p)

    elif p in common_https_ports:
        print(f"[+] Banner for {target}:{p}")
        https_banner_graber(target, p)
    elif p == 25:
        print(f"[+] Banner for {target}:{p}")
        smtp_banner_grabber(target, p)
    else:
        print(f"[+] Banner for {target}:{p}")
        banner_graber(target,p)

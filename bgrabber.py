#!/usr/bin/env python3
# Banner grabbing tool
# Author: https://github.com/Sp1derM0rph3us

import socket, sys, ssl, requests
from urllib.parse import urlparse

COMMON_HTTP_PORTS = [80, 8080, 8888, 10000, 8000, 2080]
COMMON_HTTPS_PORTS = [443, 8443, 4443]
SSL_PORTS = [443, 8443, 4443, 465, 990, 5443]

def open_socket(target, port, use_ssl=False):
    try:
        s = socket.create_connection((target, port), timeout=20)
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname=target)
        return s
    except Exception as e:
        print(f"[!] FAILED TO OPEN SOCKET: {e}")
        return None

def close_socket(sock):
    try:
        sock.close()
    except:
        pass

def send_payload(sock, payload=None):
    if not payload:
        return False
    try:
        sock.send(payload.encode())
        return True
    except Exception as e:
        print(f"[!] FAILED TO SEND PAYLOAD: {e}")
        return False

def receive_data(sock, timeout=5):
    try:
        sock.settimeout(timeout)
        data = sock.recv(4096).decode(errors="ignore").strip()
        return True, data
    except Exception as e:
        print(f"[!] FAILED TO RETRIEVE DATA: {e}")
        return False, None

def grab_with_requests(url):
    try:
        print(f"[*] Using requests to grab banner from {url}")
        resp = requests.get(url, timeout=5, verify=False)
        print(f"[+] Status code: {resp.status_code}")
        print("--- Headers ---")
        for h, v in resp.headers.items():
            print(f"{h}: {v}")
    except Exception as e:
        print(f"[!] Requests failed: {e}")

def banner_grab_socket(target, port, use_ssl=False):
    path = input("[?] Insert the path to be requested (HTTP/HTTPS only, enter '/' for root): ") \
        if port in COMMON_HTTP_PORTS + COMMON_HTTPS_PORTS else None
    payload = f"HEAD {path} HTTP/1.1\r\nHost: {target}\r\n\r\n" if path else None

    sock = open_socket(target, port, use_ssl=use_ssl)
    if not sock:
        print("[-] Failed to establish connection.")
        return

    if payload:
        send_payload(sock, payload)

    got, data = receive_data(sock)
    if got and data:
        print(data)
    else:
        print("[-] Server returned no response...")

    close_socket(sock)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [target] [optional-port]")
        sys.exit(1)

    target = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    if target.startswith(("http://", "https://")):
        grab_with_requests(target)
        print("\n-- Obliterating your privacy, as usual ;) --")
        return

    if not port:
        print("[-] Port is required for non-FQDN targets")
        sys.exit(1)

    print(f"[*] Grabbing banner from: {target}:{port}")

    use_ssl = port in SSL_PORTS

    banner_grab_socket(target, port, use_ssl=use_ssl)
    print("\n-- Obliterating your privacy, as usual ;) --")

if __name__ == "__main__":
    main()

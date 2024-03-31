#!/usr/bin/python3
# Banner grabber and general purpose brute forcing tool
# Made by: Sp1d3rM0rph3us

import socket, sys, ssl, time, re

common_http_ports = [80, 8080, 8888, 10000]
common_https_ports = [443, 8443, 4443]

def open_socket(target, p):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, p))
        return s
    
    except socket.error as e:
        print(f"[!] FAILED TO OPEN SOCKET: {e}")
        return None

def open_ssl_socket(target, p):
    try:
        s = socket.create_connection((target, p))
        context = ssl.create_default_context()
        # Ignoring cert verification because we don't care lol
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        s_sock = context.wrap_socket(s, server_hostname=target)
        return s_sock

    except ssl.SSLError as ssl_er:
        print(f"[!] FAILED TO OPEN SSL SOCKET: {ssl_er}")
        return None

    except socket.error as s_er:
        print(f"[!] FAILED TO OPEN SSL SOCKET: {s_er}")
        return None
    
def close_socket(s):
    try:
        s.close()
        return True
    except socket.error as e:
        print(f"[!] FAILED TO CLOSE SOCKET: {e}")
        return False


def close_ssl_socket(s_sock):
    try:
        s_sock.close()
        return True
    except (ssl.SSLError, socket.error) as e:
        print(f"[!] FAILED TO CLOSE SSL SOCKET: {e}")
        return False


def check_sock_state(s):
    if isinstance(s, socket.socket) and s.fileno() != -1:
        return True
    else:
        return False
        


def check_ssl_sock_state(s_sock):
    try:
        if isinstance(s_sock, ssl.SSLSocket):
            s_sock.getpeercert()
            return True

    except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
        return True

    except (ssl.SSLError, socket.error):
        pass
    return False


def send_payload(s, payload=None):
    try:
        if payload is None:
            print("No payload loaded.")
            return False
        
        else:
            s.send(payload.encode())
            return True
    except socket.error as e:
        print(f"[!] FAILED TO SEND PAYLOAD, SOCKET ERROR: {e}")
        return False

def retrv_data(s, timeout=20):
    try:
        s.settimeout(timeout)
        if check_sock_state(s):
            response = s.recv(1024).decode('utf-8').strip() 
            return True, response
        else:
            return False
    except (socket.error, socket.timeout) as e:
        print(f"[!] FAILED TO RETRIEVE DATA, ERROR: {e}")
        return False

def send_ssl_payload(s_sock, payload=None, timeout=20):
    try:
        s_sock.settimeout(timeout)
        if payload is None:
            return True
        else:
            s_sock.send(payload.encode())
            return True

    except (ssl.SSLError, socket.error, socket.timeout) as e:
        print(f"[!] FAILED TO SEND DATA, ERROR: {e}")
        return False

def retrv_ssl_data(s_sock):
    try:
        sresponse = s_sock.recv(4096).decode('utf-8').strip()
        return True, sresponse

    except (socket.error, ssl.SSLError) as e:
        print(f"[!] FAILED TO RETRIEVE DATA, ERROR: {e}")
        return False


def main():

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: ./bgrabber.py [target] [port-number] [wordlist]")
        print("Obs. Wordlist only for smtp user bruteforce.")

    else:
        target = str(sys.argv[1])
        p = int(sys.argv[2])

        print(f"[*] Grabbing banner from: {target}:{p}")

        # HTTP banner grabbing
        if p in common_http_ports:
            req = input(str("[?] Insert the path to be requested: "))
            payload = f"HEAD {req} HTTP/1.1\r\nHost: {target}\r\n\r\n"

            try:
                s = open_socket(target, p)

                if s and check_sock_state(s):
                    if send_payload(s, payload):
                        got_response, resp = retrv_data(s)
                        if got_response:
                            print(resp)
                        else:
                            print("[-] Server returned no response...")

                    else:
                        print("[-] Failed to send payload.")
                else:
                    print("[-] Failed to establish connection to target: socket is None.")
            
            except Exception as e:
                print(f"[!] Failed to perform HTTP's banner grabbing: {e}")

            finally:
                if s:
                    close_socket(s)
                print('\r\n-- Obliterating your privacy, as usual ;)')


            
        # HTTPS banner grabbing
        elif p in common_https_ports:
           
            req = input(str("[?] Insert the path to be requested: "))
            payload = f"HEAD {req} HTTP/1.1\r\nHost: {target}\r\n\r\n"

            try:
                s_sock = open_ssl_socket(target, p)

                if s_sock and check_ssl_sock_state(s_sock):
                    if send_ssl_payload(s_sock, payload):
                        got_response, resp = retrv_ssl_data(s_sock)
                        if got_response:
                            print(resp)
                        else:
                            print("[+] Server returned no response...")
                    else:
                        print("[-] Failed to send payload.")
                else:
                    print("[-] s_sock is None or in an invalid state.")

            except Exception as e:
                print(f"[!] Failed to perform SSL connection: {e}")

            finally:
                if s_sock:
                    close_ssl_socket(s_sock)
                print('\r\n-- Obliterating your privacy, as usual ;)')

        else:
            # Simple banner grabbing
                try:
                    s = open_socket(target, p)
                    
                    if s and check_sock_state(s):
                        retrv_data(s)
                    else:
                        print("[-] Failed to establish connection to target.")
                
                except Exception as e:
                    print(f"[!] Failed to perform service's banner grabbing: {e}")
                
                finally:
                    if s:
                        close_socket(s)
                    print('\r\n-- Obliterating your privacy, as usual ;)')

if __name__ == "__main__":
    main()

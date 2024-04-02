#!/usr/bin/env python3
# Xcatch user a wordlist of files to find for X-Powered-By headers in HTTP/HTTPS responses
# Script made by: Sp1derM0rph3us

import socket,ssl,sys,re

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

def retrv_ssl_data(s_sock):
    try:
        sresponse = s_sock.recv(4096).decode('utf-8').strip()
        return True, sresponse

    except (socket.error, ssl.SSLError) as e:
        print(f"[!] FAILED TO RETRIEVE DATA, ERROR: {e}")
        return False


def wordlist_gen(filename):
    try:
        with open(filename, "r") as f:
            wordlist = f.read().split()
            return wordlist
    except (FileNotFoundError, IOError) as e:
        print(f"[-] Couldn't open {filename}: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [target] [wordlist]")
        print(f"E.g {sys.argv[0]} wwww.teste.com sup3r-s1ck-w0rdl12t")
        return 0

    else:
        target = str(sys.argv[1])

        filename = str(sys.argv[2])
        if target.startswith("http://"):
            p = 80
        elif target.startswith("https://"):
            p = 443
        else:
            print("[-] You missed the protocol! http:// or https:// before targets address!")
            return -2
        target = re.sub(r'https?://', '', target)

        print(f"[*] Grabbing banner from: {target}:{p}")
        if p == 80:
            try:
                s = open_socket(target, p)

                if s and check_sock_state(s):
                    wordlist = wordlist_gen(filename)
                    for word in wordlist:
                        payload = f"HEAD {word} HTTP/1.1\r\nHost: {target}\r\n\r\n"
                        if send_payload(s, payload):
                            got_response, resp = retrv_data(s)
                            if got_response:
                                print(f"[+] Response for file {word}:")
                                if "X-Powered-By:" in resp.upper():
                                    print(resp+"\r\n")
                                else:
                                    print("X-Powered-By not present in request's header.\r\n")
                            else:
                                print("[-] Server returned no response...\r\n")
                                return -1
                        else:
                            print("[-] Failed to send payload.")
                            return -1
                else:
                    print("[-] Failed to establish connection to target: socket is None.")
                    return -1
            
            except Exception as e:
                print(f"[!] Failed to perform HTTP's banner grabbing: {e}")
                return -1

            finally:
                if s:
                    close_socket(s)
                print('\r\n-- Obliterating your privacy, as usual ;)')

        else:

            try:
                s_sock = open_ssl_socket(target, p)
                if s_sock and check_ssl_sock_state(s_sock):
                    wordlist = wordlist_gen(filename)
                    for word in wordlist:
                        payload = f"HEAD {word} HTTP/1.1\r\nHost: {target}\r\n\r\n"
                        if send_ssl_payload(s_sock, payload):
                            got_response, resp = retrv_ssl_data(s_sock)
                            if got_response:
                                print(f"[+] Response for file {word}:")
                                if 'X-powered-By' in resp.upper():
                                    print(resp+"\r\n")
                                else:
                                    print("X-Powered-By not present in request's header.\r\n")
                            else:
                                print("[-] Server returned no response...")
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


    return 0

if __name__ == "__main__":
    main()

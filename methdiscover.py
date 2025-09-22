#!/usr/bin/env python3
# Tries to discover the HTTP methods accepted by the target
import requests, sys


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [target] ")
        return 0

    else:
        try:
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
            h = {'User-Agent': ua}
            target = sys.argv[1]
            r = requests.options(target, headers=h, timeout=10)
            r.raise_for_status()
            header = r.headers.get('Allow')

            if header:

                print(f"[+] HTTP server response: {r}")
                print(f"[+] Methods accepted: {header.split(',')}")
                return 0

            else:
                print("[-] Can't retrieve server methods, they don't tell us!")


        except requests.exceptions.HTTPError as err:
            if r.status_code == 501:
                header = r.headers.get('Allow')
                return 0

            else:
                print(f'[-] Failed to retrieve accepted methods: {err}')
                return -1

        except requests.exceptions.Timeout as err:
            print(f'[-] Unable to get methods: {err}')
            return -1

        finally:
            print("\r\n-- Obliterating your privacy, as usual ;)")

    return 0

if __name__ == "__main__":
    main()

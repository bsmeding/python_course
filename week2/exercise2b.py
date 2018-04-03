#!/usr/bin/env python

import telnetlib
import getpass
import time
from pprint import pprint

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def send_command(remote_conn, cmd):
	# strip off beginning lines
	cmd = cmd.rstrip()
	#sent command
	remote_conn.write(cmd + '\n')
	time.sleep(1)
	return remote_conn.read_very_eager()
	#print output	

def login(remote_conn, username, password):
	output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
	# Sent Username
	remote_conn.write(username + '\n')
	#Wait for password
	output += remote_conn.read_until("ssword:", TELNET_TIMEOUT)
	# Sent Username
	remote_conn.write(password + '\n')	
	return output

def main():
	ip_addr = '184.105.247.70'
	username = 'pyclass'
 #	password = getpass.getpass()
	password = '88newclass'

	remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
	login(remote_conn, username, password)


	# Sent Commands to router
	output = send_command(remote_conn, "terminal length 0")
	output = send_command(remote_conn, "show ip int brief")
	print output


	# Close connection
	remote_conn.close()

if __name__ == "__main__":
	main()

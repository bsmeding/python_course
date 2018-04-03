#!/usr/bin/env python

import telnetlib
import getpass
import time
from pprint import pprint

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def main():
	ip_addr = '184.105.247.70'
	username = 'pyclass'
 #	password = getpass.getpass()
	password = '88newclass'

	remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
	output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
	# Sent Username
	remote_conn.write(username + '\n')
	#Wait for password
	output = remote_conn.read_until("ssword:", TELNET_TIMEOUT)
	# Sent Username
	remote_conn.write(password + '\n')	
	print output

	#Get login state, sleep 1 second
	time.sleep(1)
	output = remote_conn.read_very_eager()
	print output


	# Disable paging
	remote_conn.write("terminal length 0" + '\n')
	time.sleep(1)
	output = remote_conn.read_very_eager()
	print output


	# Show version
	remote_conn.write("show version" + '\n')
	time.sleep(1)
	output = remote_conn.read_very_eager()
	print output


	# Close connection
	remote_conn.close()

if __name__ == "__main__":
	main()

#!/usr/bin/env python

import telnetlib
import getpass
from pprint import pprint

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def main():
	ip_addr = '184.105.247.70'
	username = 'pyclass'
	password = getpass.getpass()

	remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)


	output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
	print output

	remote_conn.close()

if __name__ == "__main__":
	main()

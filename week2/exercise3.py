#!/usr/bin/env python

import telnetlib
import getpass
import time
from pprint import pprint

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class telnet_conn(object):
    """telnet login function to get info from router devices
    """

    def __init__(self, ip, username, password):
        """Return telnet login"""
        self.ip = ip
        self.usern = username
        self.passw = password
        
        try:
            self.remote_conn = telnetlib.Telnet(self.ip, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

    def login(self):
		output = self.remote_conn.read_until("sername:", TELNET_TIMEOUT)
		# Sent Username
		self.remote_conn.write(self.usern + '\n')
#		#Wait for password
		output += self.remote_conn.read_until("ssword:", TELNET_TIMEOUT)
		# Sent Username
		self.remote_conn.write(self.passw + '\n')
		time.sleep(1)	
		return output		

	def send_command(self, cmd):
		"""
		Sent command to device, after login
		"""
		cmd = cmd.rstrip()
		self.remote_conn.write(cmd + '\n')
		time.sleep(1)
		return self.remote_conn.read_very_eager()

def main():
	ip_addr = '184.105.247.70'
	username = 'pyclass'
 #	password = getpass.getpass()
	password = '88newclass'

	pynetrtr1 = telnet_conn(ip_addr, username, password)

	pynetrtr1.login()



	# Sent Commands to router
	#output = send_command(remote_conn, "terminal length 0")
	#output = send_command(remote_conn, "show ip int brief")
	#print output


	# Close connection
	#remote_conn.close()

if __name__ == "__main__":
	main()

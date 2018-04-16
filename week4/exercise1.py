#!/usr/bin/env python

import paramiko
import time
from pprint import pprint
from getpass import getpass

ip_addr = '184.105.247.70'
username = 'pyclass'
password = '88newclass'
port = 22

def main():
	# setup paramiko SSH connection
	remote_conn_pre = paramiko.SSHClient()
    	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	remote_conn_pre.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False, port=port)

	#Invoke shell
	remote_conn = remote_conn_pre.invoke_shell()
	remote_conn.settimeout(6.0)

	# Test output
	output = remote_conn.recv(5000)
	print(output)

	#Set terminal length
	output = remote_conn.send("terminal length 0\n")
	if remote_conn.recv_ready():
		output = remote_conn.recv(5000)
		print(output)	


	#show version
	output = remote_conn.send('show version\n')
	output = remote_conn.send('\n\n')
	time.sleep(1)
	if remote_conn.recv_ready():
		output = remote_conn.recv(5000)
		print(output)	


if __name__ == "__main__":
        main()



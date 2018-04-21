#!/usr/bin/env python

import paramiko
import time
import pexpect
from pprint import pprint
from getpass import getpass

ip_addr = '184.105.247.71'
username = 'pyclass'
password = '88newclass'
port = 22

PRINT_CMD = True
LOGGIN_BUFFER = 12345

def send_cmd(remote_conn, cmd):
	output = remote_conn.send(cmd + '\n')
	time.sleep(1)
	if remote_conn.recv_ready():
		#print("enable mode")
		output = remote_conn.recv(5000)
		if PRINT_CMD == True:
			print(output)	
	return output	

def connect(username, ip_addr, port):
	remote_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))
	return remote_conn

def main():
	# setup paramiko  SSH connection
	
	#Invoke shell
	remote_conn = connect(username, ip_addr, port)
	remote_conn.timeout = 3

	remote_conn.expect('ssword:')
	remote_conn.sendline(password)
	remote_conn.expect('#')
	router_name = (remote_conn.before)
	router_name = router_name.strip()

	#show ip int brief
	remote_conn.sendline('show ip int brief')
	remote_conn.expect(router_name + '#')

	print(remote_conn.before)

if __name__ == "__main__":
        main()



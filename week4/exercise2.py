#!/usr/bin/env python

import paramiko
import time
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

def main():
	# setup paramiko SSH connection
	remote_conn_pre = paramiko.SSHClient()
    	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	remote_conn_pre.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False, port=port)

	#Invoke shell
	remote_conn = remote_conn_pre.invoke_shell()
	remote_conn.settimeout(6.0)

	#Set terminal length
	cmd = send_cmd(remote_conn, 'terminal length 0')

	# Enable
	cmd = send_cmd(remote_conn, 'enable')

	# Current logging size
	cmd = send_cmd(remote_conn, 'show run | incl logging buffered')

	# Config mode
	cmd = send_cmd(remote_conn, 'config terminal')
	
	# Change logging buffer
	cmd = send_cmd(remote_conn, 'logging buffered 12345')

	# Exit config-mode
	cmd = send_cmd(remote_conn, 'end')

	# Current logging size
	cmd = send_cmd(remote_conn, 'show run | incl logging buffered')


if __name__ == "__main__":
        main()



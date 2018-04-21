#!/usr/bin/env python

#import paramiko
import sys
import pexpect
import re 				# re.escape
#from pprint import pprint
#from getpass import getpass

ip_addr = '184.105.247.71'
username = 'pyclass'
password = '88newclass'
port = 22

PRINT_CMD = True
LOGGIN_BUFFER = 12345

def send_cmd(remote_conn, router_name, cmd):
	remote_conn.sendline('terminal length 0')
	remote_conn.expect(router_name + '#')
	remote_conn.sendline(cmd)
	remote_conn.expect(router_name + '#')
	return remote_conn.before

def send_cfg_cmd(remote_conn, router_name, cmd):
	remote_conn.sendline("config terminal")
	remote_conn.expect(re.escape(router_name + '(config)#'))
	remote_conn.sendline(cmd)
	remote_conn.expect(re.escape(router_name + '(config)#'))
	remote_conn.sendline("end")
	remote_conn.expect(router_name + '#')	
	return remote_conn.before

def connect(username, ip_addr, port):
	remote_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))
	return remote_conn

def login(remote_conn, password):
	remote_conn.expect('ssword:')
	remote_conn.sendline(password)
	remote_conn.expect('#')
	router_name = (remote_conn.before)
	router_name = router_name.strip()
	return(router_name)

def main():
	# setup paramiko  SSH connection
	remote_conn = connect(username, ip_addr, port)
	remote_conn.timeout = 3
	remote_conn.logfile = sys.stdout

	#Login and retrive hostname
	router_name = login(remote_conn, password)

	#Get current buffer
	current_loggin_buffer = send_cmd(remote_conn, router_name, 'show run | incl logging buffered')
	print(current_loggin_buffer)

	#Get current buffer
	change_loggin_buffer = send_cfg_cmd(remote_conn, router_name, 'loggin buffered 54321')
	print(change_loggin_buffer)
	


if __name__ == "__main__":
        main()



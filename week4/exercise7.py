#!/usr/bin/env python

from netmiko import ConnectHandler
import sys
import pexpect
import re 				# re.escape
#from pprint import pprint
#from getpass import getpass




PRINT_CMD = True
LOGGIN_BUFFER = 12345


pynet1 = {
	'device_type': 'cisco_ios',
	'ip': '184.105.247.70',
	'username': 'pyclass',
	'password': '88newclass',
	'port': 22,
}
pynet2 = {
	'device_type': 'cisco_ios',
	'ip': '184.105.247.71',
	'username': 'pyclass',
	'password': '88newclass',
	'port': 22,
}
srx = {
	'device_type': 'juniper',
	'ip': '184.105.247.76',
	'username': 'pyclass',
	'password': '88newclass',
	'port': 22,
}

def send_config_cmd(connect_handler, cmd):
	output = connect_handler.send_config_set(cmd)
	return output


def send_cmd(connect_handler, cmd):
	output = connect_handler.send_command(cmd)
	return output

def main():
	# setup paramiko  SSH connection
	pynet_rtr1 = ConnectHandler(**pynet1)
	pynet_rtr2 = ConnectHandler(**pynet2)
	juniper_srx = ConnectHandler(**srx)


	#Send command
	#show_arp_rtr1 = send_cmd(pynet_rtr1, False, 'show arp')	
	output = send_cmd(pynet_rtr2, 'show run | inc logging buffered')
	print("Current buffer: " + output)

	# Change buffer size
	output = send_config_cmd(pynet_rtr2, 'logging buffered 12344')
	print("new_logg_rtr2 buffer: " + output)

	output = send_cmd(pynet_rtr2, 'show run | inc logging buffered')
	print("Current buffer: " + output)

	# change buffer size from file
	output = pynet_rtr2.send_config_from_file(config_file='buffersize.txt')
	print(output)

	output = send_cmd(pynet_rtr2, 'show run | inc logging buffered')
	print("Current buffer: " + output)


if __name__ == "__main__":
        main()



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

def config_mode(connect_handler, mode):
	if mode == 'enable':
		currentMode = (connect_handler.check_config_mode())	
		if currentMode == False:
			connect_handler.config_mode()
	elif mode == 'disable':
		currentMode = (connect_handler.check_config_mode())	
		if currentMode == True:
			connect_handler.config_mode()

def send_cmd(connect_handler, config_mode, cmd):
	#Check if privileged mode is needed
	if config_mode == True:
		config_mode(connect_handler, 'enable')
	# Send command
	output = connect_handler.send_command(cmd)

	# Disable config mode after cmd
	if config_mode == True:
		config_mode(connect_handler, 'disable')

	return output

def main():
	# setup paramiko  SSH connection
	pynet_rtr1 = ConnectHandler(**pynet1)
	pynet_rtr2 = ConnectHandler(**pynet2)
	juniper_srx = ConnectHandler(**srx)

	#Check mode
	config_mode(pynet_rtr1, 'disable')
	config_mode(pynet_rtr2, 'disable')
	config_mode(juniper_srx, 'disable')

	#outp = pynet_rtr1.find_prompt()
	#print(outp)

	#Send command
	show_arp_rtr1 = send_cmd(pynet_rtr1, False, 'show arp')	
	show_arp_rtr2 = send_cmd(pynet_rtr2, False, 'show arp')
	show_arp_srx = send_cmd(juniper_srx, False, 'show arp')

	print("ARP RTR1 : " + show_arp_rtr1)
	print("ARP RTR2 : " + show_arp_rtr2)
	print("ARP SRX : " + show_arp_srx)
if __name__ == "__main__":
        main()



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



def main():
	# setup paramiko  SSH connection
	pynet_rtr2 = ConnectHandler(**pynet2)


	#Check mode
	print("Config mode : "),
	configmode = (pynet_rtr2.check_config_mode())
	if configmode == False:
		pynet_rtr2.config_mode()
		# Check again
		print(pynet_rtr2.check_config_mode())

	try:
		configmode == True
		
			
	except:
		print("Not in enable mode!")
	

if __name__ == "__main__":
        main()



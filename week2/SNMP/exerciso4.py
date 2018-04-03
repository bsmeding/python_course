#!/usr/bin/env python
"""
This file will read SNMP OID data and print out the content

"""
from snmp_helper import snmp_get_oid, snmp_extract
import time
from pprint import pprint

COMMUNITY_STRING = 'galileo'
SNMP_PORT = 161
#IP = '184.105.247.70'




def main():

	# Define device connection
	#my_device = (IP, COMMUNITY_STRING, SNMP_PORT)
	my_devices = ['184.105.247.70', '184.105.247.71']
	my_OIDs = ['1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.1.0']

	for my_IP in my_devices:
		a_device = (my_IP, COMMUNITY_STRING, SNMP_PORT)
		#print(a_device)
		print("------------------------------")		
		for the_oid in my_OIDs:
			#snmp_data = snmp_get_oid(a_device, COMMUNITY_STRING, SNMP_PORT, oid=the_oid)
			snmp_data = snmp_get_oid(a_device, oid=the_oid)
			output = snmp_extract(snmp_data)

			print(output)

		print("------------------------------")
	print()

		#output = get_OID(device.IP, OID)
		#pprint(output)

	#Get OID Data
	#snmp_data = snmp_get_oid(my_device, oid=OID)

	#Transfrom data to readable text
	#output = snmp_extract(snmp_data)

	#output = get_OID(IP, OID)

	#Print Output
	#pprint(output)


if __name__ == "__main__":
	main()

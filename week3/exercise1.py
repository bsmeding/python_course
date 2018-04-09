#!/usr/bin/env python
"""
This file will read SNMP v3 OID data and print out the content

"""
from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail
import time
from pprint import pprint
import pickle
import datetime
import os.path
from collections import namedtuple

username =      'pysnmp'
auth_key =      'galileo1'         
encrypt_key =   'galileo1'
SNMP_PORT =     161

auth_proto =    'sha'
encrypt_proto = 'aes128'

check_file = "config_check.pkl"

# Copieed: Create namedtuple for network devices
NetworkDevice = namedtuple("NetworkDevice", "uptime last_changed run_config_changed")


#def snmp_get_oid_v3(snmp_device, snmp_user, oid='.1.3.6.1.2.1.1.1.0', auth_proto='sha', encrypt_proto='aes128', display_errors=True):
# Uptime when running config last changed
#ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   

# Uptime when running config last saved
# note any 'write' constitutes a save    
#ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   

# Uptime when startup config last saved   
#ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'


def get_last_status(file_name):
        """
        Get te last saved status of de devices.
        """


        all_devices = {}

        #Check if file exists
        if not os.path.isfile(file_name):
                return {}
        # Read file
        with open(file_name, 'rb') as f1:
                while True:
                        try:
                                all_devices = pickle.load(f1)
                        except EOFError:
                                break

        return all_devices


def save_last_status(file_name, data_dict):
        """
        save new data to file
        """

        with open(file_name, 'wb') as f2:
                pickle.dump(data_dict, f2)

def get_snmp_system_name(a_device, snmp_user):
        """
        Get SNMP data from device and return SystemName
        """
        sys_name_oid = '1.3.6.1.2.1.1.5.0'
        return snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=sys_name_oid))

def get_snmp_system_uptime(a_device, snmp_user):
        """
        Get SNMP data from device and return SystemName
        """
        sys_name_oid = '1.3.6.1.2.1.1.3.0'
        return int(snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=sys_name_oid)))

def get_snmp_running_last_changed(a_device, snmp_user):
        """
        Get SNMP data from device and return SystemName
        """
        sys_name_oid = '1.3.6.1.4.1.9.9.43.1.1.1.0'
        return int(snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=sys_name_oid)))

## copied:
def create_new_device(device_name, uptime, last_changed):
        """Create new Network Device."""
        dots_to_print = (35 - len(device_name)) * '.'
        print("{} {}".format(device_name, dots_to_print))
        print("saving new device")
        return NetworkDevice(uptime, last_changed, False)

def send_notification(device_name):
    """Send email notification regarding modified device."""

    current_time = datetime.datetime.now()

    sender = 'pynetclass-bart@twb-tech.com'
    recipient = 'bartsmeding@gmail.com'
    subject = 'Device {} was modified'.format(device_name)
    message = '''
The running configuration of {} was modified.
This change was detected at: {}
'''.format(device_name, current_time)

    if send_mail(recipient, subject, message, sender):
        print('Email notification sent to {}'.format(recipient))
        return True

def main():

        #get_last_status(check_file)

        # My devices
        pynet_rtr1 = ('184.105.247.70', 161)
        pynet_rtr2 = ('184.105.247.71', 161)

        # SNMP v3 credentials
        username =      'pysnmp'
        auth_key =      'galileo1'         
        encrypt_key =   'galileo1'
        snmp_user = (username, auth_key, encrypt_key)

        auth_proto =    'sha'
        encrypt_proto = 'aes128'        


        print('\n*** Checking for device changes ***')
        saved_devices = get_last_status(check_file)
        print("{} devices were previously saved\n".format(len(saved_devices)))       

        # Empty dict
        current_devices = {}

        # loop trough devices
        for a_device in (pynet_rtr1, pynet_rtr2):
                device_name = get_snmp_system_name(a_device, snmp_user)
                device_uptime = get_snmp_system_uptime(a_device, snmp_user)
                device_runcfg_lc = get_snmp_running_last_changed(a_device, snmp_user)
                print("\nDevice name: {}".format(device_name))
                print("Uptime: {}".format(device_uptime))
                print("Last changed: {}".format(device_runcfg_lc))
        

                # New network device
                if device_name not in saved_devices:
                    current_devices[device_name] = create_new_device(device_name, device_uptime, device_runcfg_lc)
                else:
                    # Device has been previously saved
                    saved_device = saved_devices[device_name]
                    dots_to_print = (35 - len(device_name)) * '.'
                    print("{} {}".format(device_name, dots_to_print))


                    # running-config did not change
                    if device_runcfg_lc == saved_device.last_changed:
                        print("not changed")
                        current_devices[device_name] = NetworkDevice(device_uptime, device_runcfg_lc, False)

                    # running-config changed
                    elif device_runcfg_lc > saved_device.last_changed:
                        print("CHANGED")
                        current_devices[device_name] = NetworkDevice(device_uptime, device_runcfg_lc, True)
                        send_notification(device_name)
                    else:
                        raise ValueError()                    

        # Save device to file
        save_last_status(check_file, current_devices)
        print()

if __name__ == "__main__":
        main()



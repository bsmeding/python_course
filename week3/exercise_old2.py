#!/usr/bin/env python
"""
This file will read SNMP v3 OID data and print out the content

"""
from __future__ import print_function, unicode_literals
from snmp_helper import snmp_get_oid_v3, snmp_extract
import line_graph
import time


username =      'pysnmp'
auth_key =      'galileo1'         
encrypt_key =   'galileo1'
SNMP_PORT =     161

auth_proto =    'sha'
encrypt_proto = 'aes128'

check_file = "pynet_rtr1_fa4_bw.pkl"


InterfaceBW = namedtuple("InterfaceBW", "uptime in_octets out_octets in_packets out_packets")


def get_interface_stats(snmp_device, snmp_user, stat_type, row_number):
    """
    stat_type can be 'in_octets, out_octets, in_ucast_pkts, out_ucast_pkts

    returns the counter value as an integer
    """

    oid_dict = {
        'in_octets':    '1.3.6.1.2.1.2.2.1.10',
        'out_octets':   '1.3.6.1.2.1.2.2.1.16',
        'in_ucast_pkts':    '1.3.6.1.2.1.2.2.1.11',
        'out_ucast_pkts':    '1.3.6.1.2.1.2.2.1.17',
    }

    if stat_type not in oid_dict.keys():
        raise ValueError("Invalid value for stat_type: {}" % stat_type)

    # Make sure row_number can be converted to an int
    row_number = int(row_number)

    # Append row number to OID
    oid = oid_dict[stat_type]
    oid = oid + '.' + str(row_number)

    snmp_data = snmp_get_oid_v3(snmp_device, snmp_user, oid)
    return int(snmp_extract(snmp_data))


def create_graph(graph_stats, sample_duration):
    """Generate the graph files."""

    print()
    x_labels = []
    for x_label in range(1, 13):
        x_labels.append(str(x_label * sample_duration))

    # Create the graphs
    if line_graph.twoline("pynet-rtr1-octets.svg", "pynet-rtr1 Fa4 Input/Output Bytes",
                          graph_stats["in_octets"], "In Octets", graph_stats["out_octets"],
                          "Out Octets", x_labels):
        print("In/Out Octets graph created")

    if line_graph.twoline("pynet-rtr1-pkts.svg", "pynet-rtr1 Fa4 Input/Output Unicast Packets",
                          graph_stats["in_ucast_pkts"], "In Packets", graph_stats["out_ucast_pkts"],
                          "Out Packets", x_labels):
        print("In/Out Packets graph created")
    print()



def main():


        # My devices
        a_device = ('184.105.247.70', 161)


        # SNMP v3 credentials
        username =      'pysnmp'
        auth_key =      'galileo1'         
        encrypt_key =   'galileo1'
        snmp_user = (username, auth_key, encrypt_key)

        auth_proto =    'sha'
        encrypt_proto = 'aes128'        

 
        # Fa4 is in row number5 in the MIB-2 interfaces table
        row_number = 5
        graph_stats = {
                "in_octets": [],
                "out_octets": [],
                "in_ucast_pkts": [],
                "out_ucast_pkts": [],
        }
        base_count_dict = {}       

        # Enter a loop gathering SNMP data every 5 minutes for an hour.
        # 13 samples, one every 5 minutes
        SLEEP_TIME = 5
        for count in range(12):
                print()
                time_track = count * SLEEP_TIME
                print("{:>20} {:<60}".format("time", time_track))

                # Gather SNMP statistics for each of octet/packets in and out
                for entry in graph_stats.keys():
                    snmp_retrieved_count = get_interface_stats(snmp_device, snmp_user, entry, row_number)
                    # Base counter is a dictionary with the last sample value
                    base_count = base_count_dict.get(entry)
                    if base_count:
                        # Calculate the difference from the last sample
                        calculated_diff = snmp_retrieved_count - base_count
                        # Save the data to graph_stats dictionary
                        graph_stats[entry].append(calculated_diff)
                        print("{:>20} {:<60}".format(entry, calculated_diff))
                    # Update the base counter value
                    base_count_dict[entry] = snmp_retrieved_count
                time.sleep(SLEEP_TIME)

        # Create the graphs
        create_graph(graph_stats, sample_duration=SLEEP_TIME)        

if __name__ == "__main__":
        main()



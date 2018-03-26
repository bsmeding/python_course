#!/usr/bin/env python
"""
Write a Python program using ciscoconfparse that parses this config file. 
Note, this config file is not fully valid (i.e. parts of the configuration are missing). 
The script should find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO') and for each crypto map entry print out its children.

"""
from ciscoconfparse import CiscoConfParse
import pprint


# Read files

def main():
    """
    Main application
    """
    # Set filenames
    config_file = "pynet-rtr1.conf"

    # Parse config file
    parse = CiscoConfParse(config_file)

    crypto_parents = parse.find_objects_w_child(parentspec=r"^crypto map CRYPTO", \
      childspec=r"set\spfs\sgroup2")
  

    #Loop crypto parents
    for obj in crypto_parents:
      print ""
      #print "Crypto map parent: ", obj.text
      print ""
      print obj.text

      ### Get all children
      #crypto_child = parse.find_all_children(obj.text)
      #print crypto_child
      
      for child in obj.children:
        print child.text



# Start script

if __name__ == "__main__":
    main()

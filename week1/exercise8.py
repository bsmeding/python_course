#!/usr/bin/env python
"""
Python script to  read two files, one YAML and one JSON file and print content

"""
import json
import yaml
import pprint


# Read files

def main():
    """
    Main application
    """
    # Set filenames
    list_to_yaml = "output_my_info.yaml"
    list_to_json = "output_my_info.json"


    # Open YAML
    with open(list_to_yaml) as yf:
      list_1 = yaml.load(yf)

    # Open JSON
    with open(list_to_json) as jf:
      list_2 = json.load(jf)

    # Print to screen
    print ""
    print "My YAML list:\n"
    print ""
    pprint.pprint(list_1)
    print ""
    print "My JSON list:\n"
    print ""
    pprint.pprint(list_2)


# Start script

if __name__ == "__main__":
    main()

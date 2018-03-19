#!/usr/bin/env python
"""
Python script to create a list, dict in the list and two keys

Output of the script will be one YAML and one JSON file
"""
import json
import yaml

# Create list

def main():
    """
    Main application
    """
    # Set filenames
    list_to_yaml = "my_info.yaml"
    list_to_json = "my_info.json"



    # Create list
    barts_list = ['Bart']
    barts_list.append('Smeding')
    barts_list.append({})
    barts_list[-1]['Company'] = ('YaWorks')
    barts_list[-1]['Address'] = ('Sijsjesbergweg 44')
    barts_list[-1]['numbers'] =  range(8)


    # Save to YAML
    with open(list_to_yaml, "w") as yf:
      yf.write(yaml.dump(barts_list, default_flow_style=False))


    # Save to JSON
    with open(list_to_json, "w") as jf:
      json.dump(barts_list, jf)


    # Print to screen
    print barts_list



if __name__ == "__main__":
    main()

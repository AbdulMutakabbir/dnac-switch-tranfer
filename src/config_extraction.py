#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import os
import sys
import json

# exporting project
sys.path.append(os.pardir)
from src.dnac_config import *


# In[2]:


source_path = os.pardir + os.sep + "source-switch-config.txt"
destination_path = os.pardir + os.sep + "destination-switch-config.txt"
updated_destiantion_path = os.pardir + os.sep + "updated-destination-switch-config.txt"
destiantion_source_mapping_path = os.pardir + os.sep + "destination-source-mapping-switch-config.txt"


# In[3]:


def get_config_line_number_range(lines, init_index, stop_pattern = "!"):
    init_index += 1
    for index, line in enumerate(lines[init_index:]):
        if (line.strip() == "!"):
            return (init_index+1, init_index + index)
    return (None, None)


# In[4]:


def get_all_config_meta_data(lines):
    config_ranges = []

    port_pattern = re.compile(r"(interface (\w+Ethernet)(\d+)/(\d+)/(\d+))")

    for index, line in enumerate(lines):
        if (line.strip() == "!"):
            next_line = lines[index+1]
            port_pattern_matches = port_pattern.findall(next_line)
            if (port_pattern_matches is not None) and (len(port_pattern_matches) == 1):
                ethernet_type = port_pattern_matches[0][1]
                slot = port_pattern_matches[0][2]
                sub_slot = port_pattern_matches[0][3]
                port = port_pattern_matches[0][4]
                config_range = get_config_line_number_range(lines, index)
                if (config_range[0] is not None) and (config_range[1] is not None):
                    confg_data = {
                        'start_index': config_range[0],
                        'end_index': config_range[1],
                        'ethernet_type': ethernet_type,
                        'slot': slot,
                        'sub_slot': sub_slot,
                        'port': port
                    }
                    config_ranges.append(confg_data)
                
    return config_ranges


# In[5]:


def get_all_configs(data):
    configs = []
    
    line_data = data.split("\n")
    
    config_meta = get_all_config_meta_data(line_data)
    
    for meta_data in config_meta:
        config = "\n".join(line_data[meta_data['start_index']:meta_data['end_index']])
        meta_data['config'] = config
        configs.append(meta_data)
        
    return configs


# In[6]:


def get_port_name(ethernet_type:str,slot:int,sub_slot:int,port:int):
    return f"{ethernet_type}{slot}/{sub_slot}/{port}"


# In[7]:


def get_updated_destination_config(source_data, destination_data):
    source_configs = get_all_configs(source_data)
    destination_configs = get_all_configs(destination_data)

    new_destination_config = []
    destination_config = destination_data.split("\n")
    if (len(destination_configs) == 0) or (len(source_configs) == 0):
        return destination_data, {}

    update_mapping = {}
    update_mapping["skip_source_ports"] = []

    len_source = len(source_configs)
    source_index = 0

    new_destination_config.extend(destination_config[0:destination_configs[0]['start_index']])

    for destination_index, config_info in enumerate(destination_configs):

        # add intial config part
        new_destination_config.extend(destination_config[destination_configs[destination_index-1]['end_index']:config_info['start_index']])

        source_update_info = None
        destiantion_port_name = get_port_name(config_info['ethernet_type'],
                                                config_info['slot'],
                                                config_info['sub_slot'],
                                                config_info['port'])
        update_mapping[destiantion_port_name] = source_update_info

        # skip if the destionation ehternet type in skip list
        # skip if destination port is an uplink port
        if (config_info['ethernet_type'] in SKIP_DESTINATION_ETHERNET_TYPES) or            (any(string in config_info['config'] for string in SKIP_LINES)):
            new_destination_config.append(config_info['config'])
            continue

        # get next source port
        found_next_source_port = False
        while not found_next_source_port:
            if source_index < len_source:
                source_config = source_configs[source_index]
                source_index += 1
                if len(source_config['config']):
                    source_update_info = get_port_name(source_config['ethernet_type'],
                                                       source_config['slot'],
                                                       source_config['sub_slot'],
                                                       source_config['port'])

                    # skip if source port in skip list
                    # skip if source port is uplink port
                    if(any(string in source_config['config'] for string in SKIP_LINES)):
                        update_mapping["skip_source_ports"].append(source_update_info)
                        continue

                    new_destination_config.append(source_config['config'])
                    update_mapping[destiantion_port_name] = source_update_info
                    found_next_source_port = True
            else:
                new_destination_config.append(config_info['config'])
                break

    new_destination_config.extend(destination_config[destination_configs[-1]['end_index']:])

    new_destination_config = "\n".join(new_destination_config)
    update_mapping
    return new_destination_config, update_mapping


# In[8]:


def main():
    # read source config-file data
    with open(source_path) as source_file:
        source_data = source_file.read()

    # read destination config-file data
    with open(destination_path) as destination_file:
        destination_data = destination_file.read()

    # extract mapping and new config from source and destination
    new_config, mapping = get_updated_destination_config(source_data, destination_data)

    # save update config
    with open(updated_destiantion_path, 'w') as new_destination_file:
        new_destination_file.write(new_config)
    
    # save mapping
    with open(destiantion_source_mapping_path, 'w') as mapping_file:
        json.dump(mapping, mapping_file, indent = 4)


# In[9]:


if __name__ == '__main__':
    main()


# In[ ]:





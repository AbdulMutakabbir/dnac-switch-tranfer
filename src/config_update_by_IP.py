#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
from dnacentersdk import DNACenterAPI

# exporting project
sys.path.append(os.pardir)
from src.dnac_config import *
from src.config_extraction import *


# In[2]:


SOURCE_IP = ""
DESTINATION_IP = ""

assert SOURCE_IP != ""
assert DESTINATION_IP != ""
assert len(SOURCE_IP.split(".")) == 4
assert len(DESTINATION_IP.split(".")) == 4

assert DNA_CENTER 
DNA_CENTER


# In[3]:


try:
    dna = DNACenterAPI(username=DNA_CENTER["username"], 
                   password=DNA_CENTER["password"], 
                   base_url=DNA_CENTER["host"], 
                   version='2.2.2.3', 
                   verify=False)
except:
    print("DNAC Credential Error!!!")


# # Get device config from id

# In[4]:


source_id = dna.devices.get_network_device_by_ip(SOURCE_IP).response.id
source_device_config = dna.devices.get_device_config_by_id(source_id).response


# In[5]:


destiantion_id = dna.devices.get_network_device_by_ip(DESTINATION_IP).response.id

destination_device_config = dna.devices.get_device_config_by_id(destiantion_id).response


# In[6]:


# extract mapping and new config from source and destination
new_config, mapping = get_updated_destination_config(source_device_config, destination_device_config)

# save update config
with open(updated_destiantion_path, 'w') as new_destination_file:
    new_destination_file.write(new_config)

# save mapping
with open(destiantion_source_mapping_path, 'w') as mapping_file:
    json.dump(mapping, mapping_file, indent = 4)


# In[9]:


print("Finished Updated...")
print(f"Mappling location:\t\t{destiantion_source_mapping_path}")
print(f"Updated Config Location:\t{updated_destiantion_path}")


# In[ ]:





# User Input

# Please select the lab environment that you will be using today
#     sandbox - Cisco DevNet Always-On / Reserved Sandboxes

ENVIRONMENT_IN_USE = "sandbox"

if ENVIRONMENT_IN_USE == "sandbox":
    DNA_CENTER = {
        "host": "dandboxdnac.cisco.com",
        "port": 443,
        "username": "devnetuser",
        "password": "Cisco123!"
    }

    
    
####################################################################################
#### CONFIG EXTRACTION GLOABL SCOPE ################################################
####################################################################################

SKIP_DESTINATION_ETHERNET_TYPES = ["TenGigabitEthernet",
                                   "AppGigabitEthernet",
                                   "FortyGigabitEthernet"]
SKIP_SOURCE_ETHERNET_TYPES = ["GigabitEthernet"]
SKIP_LINES = ["switchport mode trunk"]

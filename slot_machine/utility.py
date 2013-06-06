#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Source File: utility.py
# Author Name: Justin Hellsten
# Last Modified By: Justin Hellsten
# Last Modified Date: June 6, 2013
#
# Program Description: 
#
#        This file holds utility functions that will help build game or application projects in Python. 
#
# Version 0.1:
#
#        - Configuration file read/write
#        - System configuration file override
#        - initialize from system configuration file
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__CONFIG_DIR = ''
__CONFIG_MAP = {}
    
def init():
    # Scan local directory for configuration file. Omits if it is not there. This ensures some sort of configuration file is set and
    # there will be no need to call set_config_file().   
    try:
        with open('config.cfg'): pass
        __CONFIG_DIR = 'config.cfg'
        set_config_file(__CONFIG_DIR)
    except IOError:
        return
       
def get_config_value(key, default):
    value = __CONFIG_MAP.get(key)
    return value if value else default
    
def set_config_file(directory):
    global __CONFIG_DIR, __CONFIG_MAP
    __CONFIG_DIR = directory
    __CONFIG_MAP = __populate_map(open(__CONFIG_DIR, 'r'))

def get_config_path():
    return __CONFIG_DIR

def __populate_map(configFile):
    line = ''
    configMap = {}
    for line in configFile.readlines():
        tokens = line.strip().split('=')
        if len(tokens) == 2:
            configMap[tokens[0]] = tokens[1]
            
            
    return configMap


    
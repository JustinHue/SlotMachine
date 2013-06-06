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

__SYSTEM_CONFIG_DIR = 'config/system.cfg'
__SYSTEM_CONFIG_FILE = None
__SYSTEM_CONFIG_MAP = {}

__CONFIG_DIR = ''
__CONFIG_FILE = None
__CONFIG_MAP = {}
    
def init():
    override_system_config(__SYSTEM_CONFIG_DIR)
    
def get_config_value(key, default):
    __get_config_value(__CONFIG_MAP)
    
def override_system_config(directory):
    __SYSTEM_CONFIG_DIR = directory
    __SYSTEM_CONFIG_FILE = open(__SYSTEM_CONFIG_DIR, 'r')
    __SYSTEM_CONFIG_MAP = __populate_map(__SYSTEM_CONFIG_FILE)    
    
def set_config_file(directory):
    __CONFIG_DIR = directory
    __CONFIG_FILE = open(__CONFIG_DIR, 'r')
    __CONFIG_MAP = __populate_map(__CONFIG_FILE)
    

def __get_config_value(key, default, dictionary):
    value = dictionary.get(key)
    return value if value else default

def __populate_map(configFile):
    line = ''
    configMap = {}
    
    for line in configFile.readlines():
        tokens = line.strip().split('=')
        if len(tokens) == 2:
            configMap[tokens[0]] = tokens[1]
            
    return configMap


    
'''
Created on Oct 4, 2014

@author:  Grzegorz Pasieka

Copyright (C) 2014  Grzegorz Pasieka

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import os
import git_wrapper
import ConfigParser

P4CONFIG_PATH = git_wrapper.get_topdir()+"/.git/p4config"

def get_all_config():
    result = dict()
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    
    for section in config_parser.sections():
        result[section] = config_parser.items(section)
    
    return result

def get_branch_config(branch_name):
    result = dict()
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    
    result[branch_name] = config_parser.items(branch_name)
    
    return result

def set_branch_config(branch_name, p4_config):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    av_sections = config_parser.sections()
    
    if branch_name not in av_sections:
        config_parser.add_section(branch_name)
    
    for name, value in p4_config.__dict__.iteritems():
        config_parser.set(branch_name, name, value)
                
    with open(P4CONFIG_PATH, "w+") as config_file:
        config_parser.write(config_file)
        
def set_branch_config_option(branch_name, option_name, option_val):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    av_sections = config_parser.sections()
    
    if branch_name not in av_sections:
        print "ERROR: no such P4 branch"
        return
    
    if option_name != None and option_val != None:
        config_parser.set(branch_name, option_name, option_val)
                
    with open(P4CONFIG_PATH, "w+") as config_file:
        config_parser.write(config_file)
        
def new_branch_config(branch_name, p4_config):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)    
    av_sections = config_parser.sections()
    
    if branch_name in av_sections:
        print "ERROR: branch is already P4 branch. Use git-p4 config to reconfigure it"
        return
    else:
        config_parser.add_section(branch_name)
    
    for name, value in p4_config.__dict__.iteritems():
        if value != None:
            config_parser.set(branch_name, name, str(value))
                
    with open(P4CONFIG_PATH, "w+") as config_file:
        config_parser.write(config_file)
        
def remove_branch_config(branch_name):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)    
    av_sections = config_parser.sections()
    
    if branch_name not in av_sections:
        print "ERROR: no such P4 branch"
        return
    else:
        config_parser.remove_section(branch_name)
        
def get_branch_credentials(branch_name):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    p4_port = config_parser.get(branch_name, 'port')
    p4_user = config_parser.get(branch_name, 'user')
    p4_client = config_parser.get(branch_name, 'client')
    return (p4_port, p4_user, p4_client)

def is_p4_repo():
    return os.path.exists(P4CONFIG_PATH)

def is_p4_branch(branch_name):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    
    av_sections = config_parser.sections()
    
    if branch_name in av_sections:
        return True
    else:
        return False
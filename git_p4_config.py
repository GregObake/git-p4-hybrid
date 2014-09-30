'''
Created on Aug 18, 2014

@author: Grzegorz Pasieka (grz.pasieka@gmail.com)

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
import subprocess
import ConfigParser

GIT_TOPDIR = subprocess.check_output('git rev-parse --show-toplevel', shell=True)
P4CONFIG_PATH = GIT_TOPDIR.strip('\n')+"/.git/p4config"
print P4CONFIG_PATH

def git_p4_config_list():
    if False == os.path.exists(P4CONFIG_PATH):
        print "No config file"
        return
    else:
        with open(P4CONFIG_PATH, "r") as config_file:
            print config_file.read()

def git_p4_config_write(options):    
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    
    av_sections = config_parser.sections()
    
    if options.branch not in av_sections:
        config_parser.add_section(options.branch)
        
    config_parser.set(options.branch, 'port', options.port)
    config_parser.set(options.branch, 'user', options.user)
    config_parser.set(options.branch, 'client', options.client)
    if options.passwd != None:
        config_parser.set(options.branch, 'passwd', options.passwd)
                
    with open(P4CONFIG_PATH, "w+") as config_file:
        config_parser.write(config_file)
        
def get_branch_config(branch_name):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    p4_port = config_parser.get(branch_name, 'port')
    p4_user = config_parser.get(branch_name, 'user')
    p4_client = config_parser.get(branch_name, 'client')
    return (p4_port, p4_user, p4_client)
    
def git_p4_config(options):
    if options.list == True:
        git_p4_config_list()
    else:
        git_p4_config_write(options)

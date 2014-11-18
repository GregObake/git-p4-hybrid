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

import config_wrapper
import git_wrapper
from p4_wrapper import p4_wrapper

## Configure git-p4 hybrid branch
#
# @param options config command options
# list - list selected branch configuration
# list_all - list configuration for all branches
# branch - branch name, if None current branch is taken
# port - p4 server addr
# user - p4 user
# client - p4 workspace name
# root - p4 root directory path
# passwd - p4 password
def git_p4_config(options):
    if False == config_wrapper.is_p4_repo():
        print "ERROR: No P4 branch in this repository"
        return
    
    #List all p4 branches configuration
    if options.list_all == True:
        git_p4_config_list(None)
        return
    
    #Set branch for next operations & check it
    branch_name = ""    
    if options.branch == None:
        branch_name = git_wrapper.get_current_branch()
    else:
        branch_name = options.branch        
    if config_wrapper.is_p4_branch(branch_name) == False:
        print "ERROR: "+branch_name+" is not P4 branch"
        return
    
    #List selected p4 branch configuration 
    if options.list == True:
        git_p4_config_list(branch_name)
    else:
        p4config = []
        not_p4conf = ["branch", "subcommand", "list", "list_all", "passwd"]
        for name, value in options.__dict__.iteritems():
            if name not in not_p4conf and value != None:
                p4config.append((name, value))
            
        git_p4_config_write(branch_name, p4config)
        
def git_p4_config_list(branch_name):
    if branch_name == None:
        print config_wrapper.get_all_config()
    else:
        print config_wrapper.get_branch_config(branch_name)
        
def git_p4_config_write(branch_name, p4config):
    p4w = p4_wrapper()
    
    (p4port, p4user, p4client) = config_wrapper.get_branch_credentials(branch_name)
    p4w.p4_login(p4port, p4user, p4client)
    
    p4config_old = p4w.p4_client_read()
    config_wrapper.set_branch_config(branch_name, p4config)
    p4config_new = config_wrapper.get_branch_config(branch_name)
    p4w.p4_client_write(p4config_new)
    #TODO: add restoring previous config if write was not successfull
    p4w.logout()
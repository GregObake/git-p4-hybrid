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

def git_p4_config(options):
    if False == config_wrapper.is_p4_repo():
        print "ERROR: No P4 branch in this repository"
        return
    
    #List all p4 branches configuration
    if options.list_all == True:
        git_p4_config_list(None)
        return
    
    #Set branch for next operations & check it
    current_branch = ""    
    if options.branch == None:
        current_branch = git_wrapper.get_current_branch()
    else:
        current_branch = options.branch        
    if config_wrapper.is_p4_branch(current_branch) == False:
        print "ERROR: "+current_branch+" is not P4 branch"
        return
    
    #List selected p4 branch configuration 
    if options.list == True:
        git_p4_config_list(current_branch)    
    
    #else:
    #    git_p4_config_write(options)
        
def git_p4_config_list(branch_name):
    if branch_name == None:
        print config_wrapper.get_all_config()
    else:
        print config_wrapper.get_branch_config(branch_name)
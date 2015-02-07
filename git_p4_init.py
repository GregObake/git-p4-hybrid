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
from p4_wrapper import p4_wrapper
from p4_wrapper import p4_client_config
import git_wrapper
import config_wrapper
from git_p4_sync import git_p4_sync

## Initialize git-p4 hybrid branch
#
# @param options init command options
# branch - branch name, if None current branch is taken
# port - p4 server addr
# user - p4 user
# client - p4 workspace name
# root - non-default p4 root directory
# passwd - p4 password
# nosync - do not sync any changelist
# sync commit_from, commit_to -sync range 

def git_p4_init(options):
    p4w = p4_wrapper()
    #Login to workspace
    p4w.p4_login(options.port, options.user, options.client, options.passwd)
    #Read client spec
    (res, p4conf) = p4w.p4_client_read()
    p4w.save_state()
    
    if not res:
        return
    #Add client to config
    config_wrapper.new_branch_config(options.branch, p4conf)
    #change root & write client config to p4 & config file
    new_root = ""
    if options.root == None:
        new_root = git_wrapper.get_topdir()+"/.git/p4repo_"+options.branch
        os.mkdir(new_root)
    else:
        new_root = options.root

    p4conf._root =  new_root
    p4w.p4_client_write(p4conf)
    
    p4conf._port = options.port
    p4conf._user = options.user
    p4conf._passwd = options.passwd    
    config_wrapper.set_branch_config(options.branch, p4conf)
    
    if options.nosync != True:
        git_p4_sync(options)
    else:        
        print "Initialized empty git-p4 repository"
    #TODO: set p4 head
        
    p4w.p4_logout()
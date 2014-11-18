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
import p4_wrapper
import git_wrapper
import config_wrapper

## Initialize git-p4 hybrid branch
#
# @param options init command options
# branch - branch name, if None current branch is taken
# port - p4 server addr
# user - p4 user
# client - p4 workspace name
# passwd - p4 password
def git_p4_init(options):
    p4w = p4_wrapper()
    #Login to workspace
    p4w.p4login(options.port, options.user, options.client)
    #Read client spec
    p4conf = p4w.p4_client_read()
    #Add client to config
    config_wrapper.new_branch_config(options.branch, p4conf.get_all_properties())
    #change root & write client config to p4 & config file
    new_root = git_wrapper.get_repo_topdir()+"/.git/"+options.branch #TODO: per branch inner p4 repo?
    os.mkdir(new_root)
    p4conf.set_property("Root", new_root)
    p4w.p4_client_write(p4conf)
    config_wrapper.set_branch_config(options.branch, p4conf.get_all_properties())    
    #TODO: get from/to changelists numbers
    #TODO: sync files into inner p4 repo
    #TODO: copy every changelist to git repo, commit it & prepare proper commit message
    #TODO: set p4 head
        
    p4w.p4_logout()
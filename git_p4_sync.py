'''
Created on Aug 19, 2014

@author:  Grzegorz Pasieka (grz.pasieka@gmail.com)

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
from p4_wrapper import p4_wrapper, p4_client_config
import git_wrapper
import subprocess
import os
from __builtin__ import bool

## Sync p4 commmits to git branch
#
# @param options sync command options
# TODO: add some rebasing/merging options for existing commits that were not synced to p4
def git_p4_sync(options):
    pass

## Sync one p4 commmit to git branch
#
# @param changelist p4 changelist number
# @param file_count number of files to sync for progress tracking
# Only for internal use p4 must be logged in
def _git_p4_sync(path, changelist, file_count):
    p4w = p4_wrapper()
    p4w.load_state()
    
    if not p4w.is_logged():
        return False    
    
    (res, filelist) = p4w.p4_sync(path, changelist._ch_no, True, True, file_count)
    
    if not res:
        return False
    
    command = ""
    git_topdir = git_wrapper.get_topdir()
    for synced_file in filelist:        
        if synced_file._action == "add" or synced_file.action == "edit":
            command = "cp "+filelist._real_path+" "+git_topdir+p4w.strip_p4root(filelist._real_path)
        elif synced_file._action == "delete":
            command = "rf "+filelist._real_path+" "+git_topdir+p4w.strip_p4root(filelist._real_path)
            
        comm_res = subprocess.call(command, stdout=None, stderr=None)
        #TODO: add cp process tracker
    
    os.chdir(git_topdir)
    command = "git add -A"
    comm_res = subprocess.call(command, stdout=None, stderr=None)
    
    if comm_res != 0:
        return False
    
    command = "git commit -m\""+changelist.make_commit_msg()+"\""
    comm_res = subprocess.call(command, stdout=None, stderr=None)
    
    return not bool(comm_res)
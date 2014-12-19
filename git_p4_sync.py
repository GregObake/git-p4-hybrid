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
from p4_wrapper import p4_wrapper, p4_client_config, p4_changelist
import git_wrapper
import config_wrapper
import subprocess
import os
from __builtin__ import bool

## Sync p4 commmits to git branch
#
# @param options sync command options
# TODO: add some rebasing/merging options for existing commits that were not synced to p4
def git_p4_sync(options):
    p4w = p4_wrapper()
    p4w.load_state()
    
    #Login
    if not p4w.is_logged():
        (p4port, p4user, p4client) = config_wrapper.get_branch_credentials(options.branch)
        res = p4w.p4_login(p4port, p4user, p4client, None)        
        if not res:
            print "FATAL: Problem during login. Aborting git p4 sync"
            return False
        else:
            p4w.p4_client_read()
    
    #parse workspace mapping
    paths = []
    #print p4w._p4config.get_all_properties()
    for depot_path in p4w._p4config._View.iterkeys():
        if depot_path[1] != '-':
            paths.append(depot_path)
    #TODO: map changelist_no -> ws_path must be created to support mulit path commits
    #last changelist no
    last_commit = p4_changelist()
    last_commit_val = git_wrapper.get_last_commit_descr()
    last_commit_no = None
    if last_commit_val != None:
        last_commit.from_commit_msg(last_commit_val)
        last_commit_no = last_commit._ch_no
    
    path_changelist_dict = dict()
    for path in paths:        
        (res, changelists) = p4w.p4_changelists(path, last_commit_no)
        if last_commit_val != None:
            changelists = changelists[1:]
        path_changelist_dict[path] = changelists
        
    return _git_p4_sync(path_changelist_dict)
    
## Sync p4 commmits to git branch
#
# @param path_changelist_dict dictionary path -> list of changelists
def _git_p4_sync(path_changelist_dict):
    #Get changelists
    
    for path, changelists in path_changelist_dict.iteritems():
        for change in changelists:
            res =_git_p4_sync_one(path, change, 0)
            #TODO: add filecount
            if not res:
                return res
    
    return res

## Sync one p4 commmit to git branch
#
# @param path path to sync
# @param changelist p4 changelist number
# @param file_count number of files to sync for progress tracking
# Only for internal use p4 must be logged in
def _git_p4_sync_one(path, changelist, file_count):
    p4w = p4_wrapper()
    p4w.load_state()
    
    if not p4w.is_logged():
        return False    
    #TODO: for now track_progress if false
    (res, filelist) = p4w.p4_sync(path, changelist._ch_no, True, False, file_count)
    
    if not res:
        return False
    
    command = ""
    git_topdir = git_wrapper.get_topdir()
    os.chdir(p4w._p4config._Root)
    print os.getcwd()
    for synced_file in filelist:        
        if synced_file._action == "add" or synced_file._action == "edit":
            command = "cp --parents -f "+p4w.strip_p4root(synced_file._real_path)[1:]+" "+git_topdir
        elif synced_file._action == "delete":
            command = "rm -f "+git_topdir+p4w.strip_p4root(synced_file._real_path)
            #TODO: add removing empty dirs after this
            
        cp_proc = subprocess.Popen(command, stdout=None, stderr=None, shell=True)
        print command
        cp_proc.communicate()
        #TODO: add cp process tracker
    
    os.chdir(git_topdir)
    ret = git_wrapper.add_all_changes()
    
    if ret != 0:
        return False
    
    ret = git_wrapper.commit(changelist)
    
    if ret != 0:
        return False
    
    ret = git_wrapper.tag(path, changelist)
    
    return not bool(ret)
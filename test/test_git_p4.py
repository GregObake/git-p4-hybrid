'''
Created on Dec 2, 2014

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
import sys

sys.path.append(os.path.abspath(os.getcwd()+"/.."))
from git_p4_init import git_p4_init
import git_wrapper 
import subprocess
import argparse
import shutil

#globals
p4port = ""
p4user = ""
p4client = ""
p4passwd = "zaq12WSX"
calling_dir = ""

def main(argv):
    global p4port
    global p4user
    global p4client
    global p4passwd
    global calling_dir
    
    calling_dir = os.getcwd()
    
    test_prepare()
    test_git_p4_init()
    test_clean()
    
#     (p4port, p4user, p4client) = get_branch_credentials("test-branch")
#     p4w = p4_wrapper()
#     res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
#     if not res:
#         return False
#     
#     (res, changes_all) = p4w.p4_changelists() 
#     
#     git_p4_sync._git_p4_sync("//test_depot", changes_all[1], 0)

def test_git_p4_init():
    options = argparse.Namespace()
    options.__setattr__("subcommand", "init")
    options.__setattr__("port", "localhost:1818") 
    options.__setattr__("user", "g.pasieka")
    options.__setattr__("client", "test_depot_g.pasieka")
    options.__setattr__("passwd", "zaq12WSX")
    options.__setattr__("branch", "test-branch")
    options.__setattr__("root", None)
    options.__setattr__("nosync", False)
    options.__setattr__("sync", None)
    
    git_p4_init(options)
    
    if git_wrapper.get_current_branch() != options.branch:
        print "ERROR bad branch name after git-p4 init"
        return False
    if git_wrapper.check_head_CL_tag() == None:
        print "ERROR no tag on last commit"
        return False
    if len(git_wrapper.get_all_commit_descr()) <= 1:
        print "ERROR some changelists were not commited"
        return False
    
    return True
    
def test_prepare():
    #change working dir to separate test_proj
    global calling_dir
    os.chdir(calling_dir)
    test_dir = os.path.abspath("../../git-p4_test")
    if os.access(test_dir, os.R_OK or os.W_OK):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    os.chdir(test_dir)
    
    #create git repository here
    subprocess.call("git init", stdout=None, shell=True)
    subprocess.call("git checkout -b test-branch", stdout=None, shell=True)
    
def test_clean():
    global calling_dir
    os.chdir(calling_dir)
    test_dir = os.path.abspath("../../git-p4_test")
    if os.access(test_dir, os.R_OK or os.W_OK):
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    main(sys.argv)
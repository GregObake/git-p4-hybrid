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
import git_p4_sync
from p4_wrapper import p4_wrapper
from config_wrapper import get_branch_credentials

#globals
p4port = ""
p4user = ""
p4client = ""
p4passwd = "zaq12WSX"

def main(argv):
    global p4port
    global p4user
    global p4client
    global p4passwd
    
    #change working dir to separate test_proj
    test_dir = os.path.abspath("../../test_proj")
    os.chdir(test_dir)
        
    (p4port, p4user, p4client) = get_branch_credentials("test-branch")
    p4w = p4_wrapper()
    res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
    if not res:
        return False
    
    (res, changes_all) = p4w.p4_changelists() 
    
    git_p4_sync._git_p4_sync("//test_depot", changes_all[1], 0)

if __name__ == "__main__":
    main(sys.argv)
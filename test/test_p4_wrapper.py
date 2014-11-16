#! /usr/bin/python
'''
Created on Sep 20, 2014

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

import sys
import os

sys.path.append(os.path.abspath(os.getcwd()+"/.."))
from config_wrapper import get_branch_credentials
from p4_wrapper import p4_wrapper

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
        
    (p4port, p4user, p4client) = get_branch_credentials("test-branch")
    #TODO: add creating p4 for test
    
    res = test_logging()
    print "test_logging: "+str(res)
    if not res:        
        return
    
    res = test_client_read_write()
    print "test_client_read_write: "+str(res)
    res = test_changelists()
    print "test_changelists: "+str(res)
    res = test_files()
    print "test_files: "+str(res)
    res = test_sync()    
    print "test_sync: "+str(res)
    
def test_logging():
    p4w = p4_wrapper()
    res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
    if res:
        res = p4w.p4_logout()
    return res

def test_client_read_write():
    p4w = p4_wrapper()
    res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
    if not res:
        return res
    
    (res, p4conf) = p4w.p4_client_read()
    
    if res == False or p4conf == None:
        print "ERROR: p4_client_read failed"
        p4w.p4_logout()
        return False
    
    old_descr = p4conf.Description
    p4conf.Description = "New descr"
    p4w.p4_client_write(p4conf)
    (res, p4conf) = p4w.p4_client_read()
    if p4conf.Description != "New descr\n":
        print "ERROR: Description has not changed (1st)"
        res = p4w.p4_logout()
        return False
    
    p4conf.Description = old_descr
    p4w.p4_client_write(p4conf)
    (res, p4conf) = p4w.p4_client_read()
    if p4conf.Description != old_descr:
        print "ERROR: Description has not changed (2st)"
        res = p4w.p4_logout()
        return False
    
    res = p4w.p4_logout()
    return res 

def test_changelists():
    p4w = p4_wrapper()
    res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
    if not res:
        return False
    
    (res, changes_all) = p4w.p4_changelists()    
    if len(changes_all) == 0:
        print "ERROR: Getting all changelists failed"
        return False
    
    #TODO: add more tests for various cases
    
    res = p4w.p4_logout()
    return res 

def test_files():
    p4w = p4_wrapper()
    res = p4w.p4_login(p4port, p4user, p4client, p4passwd)
    if not res:
        return False
    
    (res, files_all) = p4w.p4_files()    
    if len(files_all) == 0:
        print "ERROR: Getting all files failed"
        return False

    (res, files_ch1) = p4w.p4_files(None, None, "1")    
    if len(files_ch1) != 1:
        print "ERROR: Getting files from changelist no 1 failed"
        return False
    
    (res, files_ch2) = p4w.p4_files(None, "1", "2")    
    if len(files_ch2) != 2:
        print "ERROR: Getting files from changelists no 1-2 failed"
        return False
    
    (res, files_ch3) = p4w.p4_files(None, "2", None)    
    if len(files_ch3) != 3:
        print "ERROR: Getting files from changelists no 2-now failed"
        return False
    
    res = p4w.p4_logout()
    return res 

def test_sync():
    return False
    
if __name__ == "__main__":
    main(sys.argv)

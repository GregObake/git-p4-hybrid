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

import os
import subprocess
from git_p4_config import get_branch_config
from cStringIO import StringIO

class p4_wrapper:
    def __init__(self):
        self._logged = False
        self._p4port = None
        self._p4user = None
        self._p4client = None
        self._p4client_config = dict()
        self._p4log = False        
        
    def set_p4_log(self, p4log):
        self._p4log = p4log
        
    def p4_login(self, branch_name):
        (self._p4port, self._p4user, self._p4client) = get_branch_config(branch_name)
        os.putenv('P4PORT', self._p4port)
        os.putenv('P4USER', self._p4user)
        os.putenv('P4CLIENT', self._p4client)
        res = subprocess.call('p4 login', shell=True)
        if res != 0:
            print "Problem during login"
        else:
            self._logged = True
            
    def p4_logout(self):
        res = subprocess.call('p4 logout', shell=True)
        if res != 0:
            print "Problem during logout"
        else:
            self._logged = False
            
    def p4_client_read(self):
        if self._logged == False:
            return False
        
        res = subprocess.check_output('p4 client -o', shell=True)
        self._parse_p4_client(res)
        
        return res
    
    def _parse_p4_client(self, to_parse):
        client_str_io = StringIO(to_parse)
        #first of all go to the end of long comment
        nl = client_str_io.readline()        
        while nl[0] == '#':
            nl = client_str_io.readline()
        #last line is empty
        nl = client_str_io.readline()
            
        client_str = client_str_io.read();
        client_config = dict();
        
        ind = client_str.find("Root:")
        
        
        print client_str
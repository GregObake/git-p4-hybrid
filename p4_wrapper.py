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
from datetime import datetime
from git_p4_config import get_branch_config
from cStringIO import StringIO

class p4_client_config(object):
    def add_property(self, name, value):
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)
        
        setattr(self.__class__, name, property(fget, fset))
        setattr(self, name, value)
        
    def _get_property(self, name):
        return getattr(self, name)
    
    def _set_property(self, name, value):
        setattr(self, name, value)

class p4_wrapper:
    def __init__(self):
        self._logged = False
        self._p4port = None
        self._p4user = None
        self._p4client = None
        self._p4log = False        
        self._p4conf = p4_client_config()
        
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
    
    def p4_client_write(self):
        if self._logged == False:
            return False
    
    def _parse_p4_client(self, to_parse):
        client_str_io = StringIO(to_parse)
        #first of all go to the end of long comment
        nl = client_str_io.readline()        
        while nl[0] == '#':
            nl = client_str_io.readline()
        #last line is empty
        nl = client_str_io.readline()
            
        client_str = client_str_io.read();
        
        self._parse_datetime_option(client_str, "Update:") #TODO: change to datetime
        self._parse_datetime_option(client_str, "Access:") #TODO: change to datetime
        self._parse_string_option(client_str, "Owner:")
        self._parse_string_option(client_str, "Host:")
        #client_config = self._parse_string_option(client_str, "Description:", client_config) #TODO: make method for parsing long text
        self._parse_string_option(client_str, "Root:")
        self._parse_list_option(client_str, "Options:")
        self._parse_list_option(client_str, "SubmitOptions:")
        self._parse_string_option(client_str, "LineEnd:")
        self._parse_view_option(client_str)
        
        print self._p4conf.__dict__.keys()
        print self._p4conf.__dict__.values()
        
    def _parse_string_option(self, client_str, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        words = nl.split()
        self._p4conf.add_property(arg_name[:-1], words[1])
        
    def _parse_list_option(self, client_str, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        words = nl.split()
        self._p4conf.add_property(arg_name[:-1], words[1:])
        
    def _parse_datetime_option(self, client_str, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        
        datetime_parsed = datetime.strptime(nl[len(arg_name):].strip(), "%Y/%m/%d %H:%M:%S")
        self._p4conf.add_property(arg_name[:-1], datetime_parsed)
        
    def _parse_view_option(self, client_str):
        ind = client_str.find("View:")
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline() # "View:" string
        nl = client_str_io.readline()
        
        view = dict()
        while nl.strip()!="":
            mapping = nl.split()
            view[mapping[0]] = mapping[1]
            nl = client_str_io.readline()
            
        self._p4conf.add_property("View", view)

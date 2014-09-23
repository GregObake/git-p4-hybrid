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
from p4_wrapper import p4_wrapper

def main(argv):
    p4w = p4_wrapper()
    p4w.p4_login("test-branch")
    p4w.p4_client_read()
    p4w.p4_logout()
    
if __name__ == "__main__":
    main(sys.argv)
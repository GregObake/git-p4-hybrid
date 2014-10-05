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

import p4_wrapper
from config_wrapper import new_branch_config

def git_p4_init(options):
    p4w = p4_wrapper()
    p4w.p4login(options.port, options.user. client)
    p4w.p4_client_read()
    new_branch_config(options.branch, p4w.__p4conf.get_all_properties())    
    p4w.p4_logout()
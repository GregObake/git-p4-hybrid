#! /usr/bin/python

'''
Created on Aug 18, 2014

@author: Grzegorz Pasieka (grz.pasieka@gmail.com)

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
import argparse
from git_p4_config import git_p4_config

def main(argv):        
    parser = argparse.ArgumentParser(prog='git-p4', description="git-p4 hybrid",)
    subparser = parser.add_subparsers(help='sub-command help', dest='subcommand')
    
    #TODO: list-all, list & b, others must be mutualy exclusive
    config_parser = subparser.add_parser('config', help='configure git-p4 hybrid')
    config_parser.add_argument('--list', help='list p4 config of current branch', action='store_true')
    config_parser.add_argument('--list-all', help='list p4 config of all branches', action='store_true')
    config_parser.add_argument('-b', '--branch', help='branch name')
    config_parser.add_argument('-p', '--port', help='p4 server ipaddress:port')
    config_parser.add_argument('-u', '--user', help='p4 server user')
    config_parser.add_argument('-c', '--client', help='p4 server workspace name')    
    config_parser.add_argument('-r', '--root', help='p4 workspace root')
    config_parser.add_argument('--passwd', help='p4 server password')    
    
    #PARSING OPTIONS
    options = parser.parse_args(argv[1:])
    print "DEBUG: options control"
    print options
    
    
    if options.subcommand == "config":
        git_p4_config(options)

if __name__ == "__main__":
    main(sys.argv)
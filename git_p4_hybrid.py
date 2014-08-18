#! /usr/bin/python

'''
Created on Aug 18, 2014

@author: Grzegorz Pasieka (grz.pasieka@gmail.com)
'''

import sys
import argparse
import git_p4_config

def main(argv):        
    parser = argparse.ArgumentParser(prog='git-p4', description="git-p4 hybrid",)
    subparser = parser.add_subparsers(help='sub-command help', dest='subcommand')
    
    config_parser = subparser.add_parser('config', help='configure git-p4 hybrid')
    config_parser.add_argument('-b', '--branch', help='branch name')
    config_parser.add_argument('-p', '--port', help='p4 server ipaddress:port')
    config_parser.add_argument('-u', '--user', help='p4 server user')
    config_parser.add_argument('-c', '--client', help='p4 server workspace name')
    config_parser.add_argument('--passwd', help='p4 server password')
    config_parser.add_argument('--list', help='list config', action='store_true')
    #config_parser.add_argument('-r', '--root', help='p4 workspace root')
    
    options = parser.parse_args(argv[1:])
    
    if options.subcommand == "config":
        git_p4_config(options)
    
    print options

if __name__ == "__main__":
    main(sys.argv)
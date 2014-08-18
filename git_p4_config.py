'''
Created on Aug 18, 2014

@author: Grzegorz Pasieka (grz.pasieka@gmail.com)
'''
import os
import ConfigParser

P4CONFIG_PATH = "/home/gregor/workspace/git-p4-hybrid/.git/p4config"
#P4CONFIG_PATH = os.getcwd()+"/.git/p4config"

def git_p4_config_list():
    if False == os.path.exists(P4CONFIG_PATH):
        print "No config file"
        return
    else:
        with open(P4CONFIG_PATH, "r") as config_file:
            print config_file.read()

def git_p4_config_write(options):
    if False == os.path.exists(P4CONFIG_PATH):
        open(P4CONFIG_PATH, "rw")
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(P4CONFIG_PATH)
    
    av_sections = config_parser.sections()
    
    if options.branch not in av_sections:
        config_parser.add_section(options.branch)
        
    config_parser.set(options.branch, 'port', options.port)
    config_parser.set(options.branch, 'user', options.user)
    config_parser.set(options.branch, 'client', options.client)
    if options.passwd != None:
        config_parser.set(options.branch, 'passwd', options.passwd)
        
    with open(P4CONFIG_PATH, "rw") as config_file:
        config_parser.write(config_file)
    
def git_p4_config(options):
    if options.list == True:
        git_p4_config_list()
    else:
        git_p4_config_write(options)

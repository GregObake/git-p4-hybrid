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
import io
import subprocess
from datetime import datetime
from cStringIO import StringIO
import git_wrapper

#FIXME: Add good error handling to this wrapper

class properties(object):
    def add_property(self, name, value):
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)   
             
        setattr(self.__class__, name, property(fget, fset))
        setattr(self, "_"+name, value)
        
    def _get_property(self, name):
        return getattr(self, "_"+name)
    
    def _set_property(self, name, value):
        setattr(self, "_"+name, value)
        
    def get_all_properties(self):
        result = []        
        for key, value in self.__dict__.iteritems():
            result.append( (key[1:].lower(), str(value)) )        
        return result
    
    def __str__(self):
        result = ""        
        for key, value in self.__dict__.iteritems():
            result += key[1:] +": "+str(value)+"\n"            
        return result    

class p4_client_config(properties):
    #FIXME: add members instead properties
    pass

class p4_changelist(properties):
    def __init__(self, change_no, change_date, user, workspace, desc, raw):
        self._ch_no = change_no
        self._ch_date = change_date
        self._user = user
        self._workspace = workspace
        self._desc = desc
        self._raw = raw #TODO: raw probably to delete. keeping it now for debug purpose
    def make_commit_msg(self):
        return self._workspace + "\n" + "CL: " + self._ch_no + "\n" + self._user + " " + self._ch_date + "\n" + self._desc
        
class p4_file(properties):
    def __init__(self, path, rev, action, changelist_no, real_path=None):
        self._path = path
        self._rev = rev
        self._action = action
        self._changelist_no = changelist_no
        self._real_path = real_path

class p4_wrapper:
    _s_logged = False
    _s_p4port = None
    _s_p4user = None
    _s_p4client = None
    _s_p4config = None
    
    def __init__(self):
        self._logged = False
        self._p4port = None
        self._p4user = None
        self._p4client = None
        self._p4log = True
        self._p4config = None
        
    def set_p4_log(self, p4log):
        self._p4log = p4log
        
    def print_log(self, msg):
        if self._p4log:
            print msg

    def p4_login(self, p4port, p4user, p4client, p4passwd):
        self._p4port = p4port
        self._p4user = p4user
        self._p4client = p4client
        os.putenv('P4PORT', self._p4port)
        os.putenv('P4USER', self._p4user)
        os.putenv('P4CLIENT', self._p4client)
        
        if(p4passwd != None):
            login = subprocess.Popen('p4 login', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)     
            login.communicate(input=p4passwd)
            res = login.returncode
        else:
            res = subprocess.call('p4 login', stdout=subprocess.PIPE, shell=True)
            
        if res != 0:
            print "FATAL: Problem during login"
        else:
            self._logged = True
        #FIXME: add storing p4_wrapper state in temp file        
        return not bool(res)    
            
    def p4_logout(self):
        res = subprocess.call('p4 logout', shell=True, stdout=subprocess.PIPE)
        if res != 0:
            print "FATAL: Problem during logout"
        else:
            self._logged = False
        return not bool(res)
    
    def is_logged(self):
        return self._logged
    
    def save_state(self):
        p4_wrapper._s_logged = self._logged
        p4_wrapper._s_p4port = self._p4port
        p4_wrapper._s_p4user = self._p4user
        p4_wrapper._s_p4client = self._p4client
        p4_wrapper._s_p4config = self._p4config
        
    def load_state(self):
        self._logged = p4_wrapper._s_logged 
        self._p4port = p4_wrapper._s_p4port
        self._p4user = p4_wrapper._s_p4user
        self._p4client = p4_wrapper._s_p4client
        self._p4config = p4_wrapper._s_p4config
        
    def reset_state(self):
        p4_wrapper._s_logged = False
        p4_wrapper._s_p4port = None
        p4_wrapper._s_p4user = None
        p4_wrapper._s_p4client = None
        p4_wrapper._s_p4config = None
            
    def p4_client_read(self):
        if self._logged == False:
            return (False, None)
        
        p4_read = subprocess.Popen('p4 client -o', shell=True, stdout=subprocess.PIPE)
        (read_out, read_err) = p4_read.communicate()
        if p4_read.returncode != 0:
            return (False, None)
        _p4config = self._parse_p4_client(read_out)
        
        return (True, _p4config)
    
    def p4_client_write(self, p4conf):
        if self._logged == False:
            return False
        
        output = ""
        for key, value in p4conf.__dict__.iteritems():
            output += key[1:]+":"    
            if type(value) == str:
                output += "\t"+value
            elif type(value) == list:
                output += "\t"
                for list_item in value:
                    output += list_item+" "
            elif type(value) == datetime:
                output += "\t"+value.strftime("%Y/%m/%d %H:%M:%S")
            elif type(value) == dict:
                output += "\n"
                for map_in, map_out in value.iteritems():
                    output += "\t"+map_in+" "+map_out+"\n"
            output+="\n"
        
        temp_path = git_wrapper.get_topdir()+"/.git/temp_p4_config"
        
        with open(temp_path, "w") as temp_file:
            temp_file.write(output)
            
        res = subprocess.call('p4 client -i < '+temp_path, shell=True, stdout=subprocess.PIPE)
        os.remove(temp_path)
        
        if res:
            _p4config = p4conf

        return not bool(res)
        
    def p4_changelists(self, path="//...", change_from=None, change_to=None):
        command = "p4 changes -t submitted "+path
        if change_from != None and change_to != None:
            command += "@"+change_from+",@"+change_to
        elif change_from != None and change_to == None:
            command += "@"+change_from+",@now"
        elif change_from == None and change_to != None:
            command += "@"+change_to
        res = subprocess.check_output(command, shell=True)
                
        changelists = self._parse_changelists(res)
        
        return (res, changelists)
    
    def p4_files(self, path=None, change_from=None, change_to=None):
        command = "p4 files "
        if path != None:
            command += path
        elif change_from != None and change_to != None:
            command += "@"+change_from+",@"+change_to
        elif change_from != None and change_to == None:
            command += "@"+change_from+",@now"
        elif change_from == None and change_to != None:
            command += "@"+change_to
            
        if path == None and change_from == None and change_to == None:
            command += "//..."
        res = subprocess.check_output(command, shell=True)
        
        files = self._parse_files(res)
        
        return (res, files)
        
    def p4_sync(self, path=None, changelist='#head', force=True, track_progr=False, file_count=0):
        #TODO: consider using --parallel flag
        command = "p4 sync "
        if force == True:
            command += "-f "
        
        if path == None:
            path = "//..."
        command += path
        if isinstance(changelist, str) and not changelist.isdigit():
            command += changelist
        else: 
            command += "@"+str(changelist)
        
        self.print_log(command)
        filelist = []
        if track_progr:
            filename = 'sync.log'
            with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
                syncproc = subprocess.Popen(command, shell=True, stdin=None, stdout=writer, stderr=None)                
                linecount = 0
                while syncproc.poll() is None:
                    linecount = self._parse_p4_sync_out(reader, filelist, linecount, file_count, changelist)
                # Read the remaining
                linecount = self._parse_p4_sync_out(reader, filelist, linecount, file_count, changelist)
                    
            os.remove(filename)
            res = syncproc.returncode
        else:
            res = subprocess.call(command, shell=True, stdout=subprocess.PIPE)
            
        return not (bool(res), filelist)
    
    def strip_p4root(self, path):
        return path.lstrip(self._p4config._root)
        

    def _parse_p4_sync_out(self, reader, filelist, linecount, file_no, changelist_no):
        stdoutline = reader.readline()        
        if stdoutline.strip() != "":
            sync_str = stdoutline.split()
            path = sync_str[0].split("#")[0]
            file_revision = sync_str[0].split("#")[1]
            action = self._syncstr_to_actionstr(sync_str[2])
            real_path = sync_str[3]
            synced_file = p4_file(path, file_revision, action, changelist_no, real_path)
            linecount += 1
            outstr = ""
            if file_no != 0:
                outstr = str(round(float(linecount)/file_no*100.0, 2))+"%\r"
            else:
                outstr = "File no: "+str(linecount) + " " + stdoutline
            filelist.append(synced_file)     
            self.print_log(outstr[:-1])   
            
        return linecount    

    def _syncstr_to_actionstr(self, action_str):
        if action_str == "refreshing":
            return "edit"
        elif action_str == "updating":
            return "edit"
        elif action_str == "added":
            return "add"
        elif action_str == "deleted":
            return "delete"
        else:
            return "invalid" 
    
    def _parse_p4_client(self, to_parse):
        p4conf = p4_client_config()
        client_str_io = StringIO(to_parse)
        #first of all go to the end of long comment
        nl = client_str_io.readline()
        while nl[0] == '#':
            nl = client_str_io.readline()
        #last line is Client not sure must I parse it
            
        client_str = client_str_io.read();
        
        self._parse_string_prop(client_str, p4conf, "Client:")
        self._parse_datetime_prop(client_str, p4conf, "Update:")
        self._parse_datetime_prop(client_str, p4conf, "Access:")
        self._parse_string_prop(client_str, p4conf, "Owner:")
        self._parse_string_prop(client_str, p4conf, "Host:")
        self._parse_description_prop(client_str, p4conf)
        self._parse_string_prop(client_str, p4conf, "Root:")
        self._parse_list_prop(client_str, p4conf, "Options:")
        self._parse_list_prop(client_str, p4conf, "SubmitOptions:")
        self._parse_string_prop(client_str, p4conf, "LineEnd:")
        self._parse_view_prop(client_str, p4conf)
        
        return p4conf
        
    def _parse_string_prop(self, client_str, p4conf, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        words = nl.split()
        p4conf.add_property(arg_name[:-1], words[1])
        
    def _parse_list_prop(self, client_str, p4conf, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        words = nl.split()
        p4conf.add_property(arg_name[:-1], words[1:])
        
    def _parse_datetime_prop(self, client_str, p4conf, arg_name):
        ind = client_str.find(arg_name)
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline()
        
        datetime_parsed = datetime.strptime(nl[len(arg_name):].strip(), "%Y/%m/%d %H:%M:%S")
        p4conf.add_property(arg_name[:-1], datetime_parsed)
        
    def _parse_description_prop(self, client_str, p4conf):
        ind = client_str.find("Description:")
        
        if ind == -1:
            return
        
        client_str_io = StringIO(client_str[ind:])
        nl = client_str_io.readline() # "Description:" string
        nl = client_str_io.readline()
        description = ""
        while nl.strip()!="":
            description += nl.strip('\t')
            nl = client_str_io.readline()
            
        p4conf.add_property("Description", description)
        
    def _parse_view_prop(self, client_str, p4conf):
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
            
        p4conf.add_property("View", view)
        
    def _parse_changelists(self, changelists_str):
        changelists = []
        changelists_str_io = StringIO(changelists_str)
        nl = changelists_str_io.readline()
        
        while nl.strip()!="":
            change = nl.split()
            change_no = change[1]
            change_date = datetime.strptime(change[3]+" "+change[4], "%Y/%m/%d %H:%M:%S")
            user = change[6].split('@')[0]
            workspace = change[6].split('@')[1]
            desc = nl.rsplit('\'')[1]
            changelists.append(p4_changelist(change_no, change_date, user, workspace, desc, nl))
            nl = changelists_str_io.readline()
            
        return changelists
    
    def _parse_files(self, files_str):
        files = []
        files_str_io = StringIO(files_str)
        nl = files_str_io.readline()
        
        while nl.strip()!="":
            file_str = nl.split()
            path = file_str[0].split("#")[0]
            file_revision = file_str[0].split("#")[1]
            action = file_str[2]
            changelist_no = file_str[4]
            files.append(p4_file(path, file_revision, action, changelist_no))
            nl = files_str_io.readline()          
        
        return files
        
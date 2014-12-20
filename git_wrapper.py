'''
Created on Oct 3, 2014

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

import subprocess
from cStringIO import StringIO

def get_topdir():
    return subprocess.check_output('git rev-parse --show-toplevel', shell=True).strip("\n")

def get_current_branch():
    return subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip("\n")

def get_last_commit_descr():
    commit_descr = subprocess.Popen('git log -n 1 --pretty=format:%B', shell=True, stdout=subprocess.PIPE)
    (read_out, read_err) = commit_descr.communicate()
    if commit_descr.returncode != 0:
        return None
    else:
        return read_out.split("\n")

def get_all_commit_descr():
    commit_descr = subprocess.Popen('git log --pretty=format:%B', shell=True, stdout=subprocess.PIPE)
    (read_out, read_err) = commit_descr.communicate()
    if commit_descr.returncode != 0:
        return []
    else:
        commit_list = []
        commit_str_io = StringIO(read_out)
        nl = commit_str_io.readline()
        while nl != "":
            commit_list.append(nl)
            nl = commit_str_io.readline()
        return commit_list
    
def add_all_changes():
    command = "git add -A"
    git_proc = subprocess.Popen(command, stdout=None, stderr=None, shell=True)
    git_proc.communicate()    
    return git_proc.returncode

def commit(changelist):
    command = "git commit -m\""+changelist.make_commit_msg()+"\""
    git_proc = subprocess.Popen(command, stdout=None, stderr=None, shell=True)
    git_proc.communicate()
    return git_proc.returncode

def tag_CL(path, changelist):
    command = "git tag_CL -a CL_"+changelist._ch_no+" -m\"Synced "+path+"@"+changelist._ch_no+"\""
    git_proc = subprocess.Popen(command, stdout=None, stderr=None, shell=True)
    git_proc.communicate()
    return git_proc.returncode

def check_last_CL_tag():
    command = "git describe --match=CL_* HEAD"
    git_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    (CL_tag, err) = git_proc.communicate()
    if git_proc.returncode == 0:
        return CL_tag
    else:
        return None

def check_head_CL_tag():
    command = "git describe --match=CL_* --exact-match HEAD"
    git_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    (CL_tag, err) = git_proc.communicate()
    if git_proc.returncode == 0:
        return CL_tag
    else:
        return None

def get_commit_distance(l_commit, r_commit):
    command = "git log --oneline "+l_commit+".."+r_commit
    git_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    (git_log, err) = git_proc.communicate()
    if git_proc.returncode == 0:
        return git_log.count("\n")
    else:
        return 0
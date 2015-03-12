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
from datetime import datetime
import re

class git_commit:
    def __init__(self, commit_no="", author="", email="", date_time=datetime.now(), descr=""):
        self._commit_no = commit_no
        self._author = author
        self._email = email
        self._date_time = date_time
        self._descr = descr
        
    def __str__(self):
        return self._commit_no + "\n" + self._author + "\n" + self._email + "\n" +\
            self._date_time.strftime("%a %b %d %H:%M:%S %Y") + "\n" + self._descr

def get_topdir():
    return subprocess.check_output('git rev-parse --show-toplevel', shell=True).strip("\n")

def get_current_branch():
    return subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip("\n")

def get_last_commit():
    commit_descr = subprocess.Popen('git log -n 1 --format=format:"commit %H%nAuthor: %aN <%aE>%nDate: %ad%n%B"', shell=True, stdout=subprocess.PIPE)
    (read_out, read_err) = commit_descr.communicate()
    if commit_descr.returncode != 0:
        return None
    else:
        commit_str_io = StringIO(read_out)
        git_log = commit_str_io.read()
        return _parse_git_log(git_log)[0]

def get_all_commits():
    commit_descr = subprocess.Popen('git log --format=format:"commit %H%nAuthor: %aN <%aE>%nDate: %ad%n%B"', shell=True, stdout=subprocess.PIPE)
    (read_out, read_err) = commit_descr.communicate()
    if commit_descr.returncode != 0:
        return []
    else:
        commit_str_io = StringIO(read_out)
        git_log = commit_str_io.read()
        return _parse_git_log(git_log)
    
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
    command = "git tag -a CL_"+changelist._ch_no+" -m\"Synced "+path+"@"+changelist._ch_no+"\""
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
    
def _parse_git_log(log_str):
    commit_ls = []
    gitlog_pattern = "^commit (\w{40})\nAuthor:\s+(\S+)\s+\<(\S+)\>\nDate:\s+([^\n]+)\n"    
    log_regexed= re.split(gitlog_pattern, log_str, flags=re.DOTALL|re.MULTILINE)
    
    for index in range(1, len(log_regexed), 5):
        #in Python 2.7 cannot use %z for timezone so string must be cut
        commit_date = datetime.strptime(log_regexed[index+3][:-6], "%a %b %d %H:%M:%S %Y")
        commit_obj = git_commit(log_regexed[index], log_regexed[index+1], log_regexed[index+2],
                                commit_date, log_regexed[index+4].rstrip())
        commit_ls.append(commit_obj)
    return commit_ls
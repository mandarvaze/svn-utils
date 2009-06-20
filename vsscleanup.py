#!/usr/bin/env python
#
#       vsscleanup.py
#       
#       Copyright 2009 Mandar Vaze <mandarvaze@gmail.com>
#       
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# How to use ?
# Update the following variables to match your setup
# checkoutdir - This is where you have done "getlatest" from VSS
#               Although it is called Checkout, DO NOT check out from VSS, use "Get Latest" instead
# dircmd - Lists the types of files you want to remove from VSS before you start the migration
#        - This helps in reducing the size of DB to be processed.
#        - One can also add .exe and .dll if needed (unless they are needed files form 3rd party)
# searchstr - This is location where you have done "Get Latest" from the VSS 
#           - Same value as "checkoutdir" except this is regex starting with 'r' and enclosed between 3 double quotes
# cmd - Point to the ss.exe
# SSDIR - The location of your VSS Database (Folder containing srcsafe.ini)
# SSUSER and SSPWD - Source Safe username and password - Should have Admin rights

import re
import os
import sys
import subprocess
from time import strftime

checkoutdir = "D:\\VSSGetLatest\\project\\checkout"
timestamp = strftime("%Y-%m-%d-%H-%M-%S")
logfilename = "vsscleanup-%s.log" % timestamp
badfilename = "badfiles-%s.txt" % timestamp
    
def findfiles():
    # Update this list with the extensions you do not want to migrate to SVN
    dircmd = "dir /s/B *.pdb *.cache *.nlb *.obj *.ncb *.bsc *.pch *.sbr *.idb *.vssscc *.vspscc"
    file  = open(badfilename,"wb")
    proc = subprocess.Popen(dircmd,cwd=checkoutdir,shell=True, stdout=subprocess.PIPE)
    list = proc.communicate()[0]
    file.write(list)
    file.close()
    return list

def fixpaths(lst):
    searchstr = r"""D:\\VSSGetLatest\\project\\checkout"""
    p = re.compile(searchstr)
    files = lst.split("\r\n")
    for file in files:
        filename = p.sub('$',file)
        if (len(filename) != 0):
            print "Destroying:" + filename
            ssdestroy(filename)
            print "Done"
    return

def ssdestroy(filename):
    # Update following line to point to your VSS install folder, containing ss.exe, which is cmd line interface to VSS
    cmd = "C:/vss/win32/ss Destroy " + "\""  + filename + "\""
    print cmd
    proc = subprocess.Popen(cmd,env={'SSDIR':"D:\\VSSdata4Migration\\project",'SSUSER':"admin",'SSPWD':"adminpass"},
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    print proc.communicate('Y\n')[0]
    return

def main():
    lst = findfiles()
    if (len(lst) != 0):
        fixpaths(lst)
    
if __name__ == "__main__":
    f = open(logfilename,"a")
    f.write("Begin Log at : %s\n" % strftime("%Y-%m-%d %H:%M:%S"))
    errcode = main()
    f.write("End Log at : %s\n" % strftime("%Y-%m-%d %H:%M:%S"))
    f.close()
    sys.exit(errcode)

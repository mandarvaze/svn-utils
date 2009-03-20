#!/usr/bin/env python

#
#       commit-email.py
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

'''
You can call this script from post-commit hook as follows :
/usr/share/subversion/hook-scripts/commit-email.py "$REPOS" "$REV" commit-watchers@your.org
'''

import smtplib
import os
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from time import strftime
import traceback

sender = "post-commit-hook@svnserver"
receivers = []
subject = "Subversion commit notification"
smtpserver = "127.0.0.1"

def send_mail(send_from, send_to, subject, text, server="localhost"):
  assert type(send_to)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )
  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

def main():

  try:
    argc = len(sys.argv)
    repository = sys.argv[1]
    revision = sys.argv[2]
# Rest of the arguments is a list of email addresses.
    for i in range(3,argc):
        receivers.append(sys.argv[i])

# Get the diff from svnlook
    diffcmd = "svnlook diff " + repository + " -r " + revision
    diff = os.popen(diffcmd).read()

    namecmd = "svnlook info " + repository + " -r " + revision
    infolines = os.popen(namecmd).read()

    info = infolines.splitlines()
    name= info[0]
    date = info[1]
    comment = info[3]

    emailbody = (
               "Committed By: " + name + "\r\n" +
               "Date: " + date + "\r\n" +
               "Comment: " + comment + "\r\n" +
               "Repository: " + repository + "\r\n" +
               "Revision: " + revision + "\r\n" +
               "Diff:\r\n" +
               diff + "\r\n"
               )

    send_mail(sender, receivers, subject, emailbody, smtpserver)

  except:
    traceback.print_exc(file=sys.stderr)
    return 1

  return 0

if __name__ == "__main__":
# Following code is left commented, in case you need to enable logging.
# Add f.write statements in the code, where ever needed.
#  f = open('/tmp/svn-postcommit.log', 'a+')
#  f.write("-- Begin Log at %s --\n" % strftime("%Y-%m-%d %H:%M:%S"))
  exitcode = main()
#  f.write("\n-- End Log at %s --\n" % strftime("%Y-%m-%d %H:%M:%S"))
#  f.close()
  sys.exit(exitcode)

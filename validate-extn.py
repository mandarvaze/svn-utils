#!/usr/bin/env python
#
#       validate-extn.py
#
#       Copyright 2009 Mandar Vaze (mandarvaze@gmail.com)
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

# Following script can be called from subversion's pre-commit hook script, as follows :
# /usr/share/subversion/hook-scripts/validate-extn.py "$REPOS" "$TXN" || exit 1
#

import sys
import traceback
import subprocess
import re
from time import strftime
from optparse import OptionParser

def command_output(cmd):
    " Capture a command's standard output. "
    return subprocess.Popen(
    cmd.split(), stdout=subprocess.PIPE).communicate()[0]

def filename(line):
    return line[4:]

def added_or_updated(line):
    return line and line[0] in ("A", "U")

def has_space(fname):
    reobj = re.compile(r"""\s""")
    if (reobj.search(fname) == None):
        return 0
    else:
        return 1

def disallowed_extn(fname):
    reobj = re.compile(r"""^.+\.((obj)|(lib)|(dll)|(exe)|(jar)|(pdb)|(idb)|(pch)|(bsc)|(ncb)|(ilk)|(sbr))""")
    if (reobj.search(fname) != None):
        return 1
    else:
        return 0

def main():
  usage = """usage: %prog REPOS TXN
Run pre-commit options on a repository transaction."""

  parser = OptionParser(usage=usage)
  parser.add_option("-r", "--revision",
                    help="Test mode. TXN actually refers to a revision.",
                    action="store_true", default=False)
  try:
      (opts, (repos, txn_or_rvn)) = parser.parse_args()
      look_opt = ("--transaction", "--revision")[opts.revision]
      look_cmd = "svnlook %s %s %s %s" % ("%s", repos, look_opt, txn_or_rvn)
      rawcmdout = command_output(look_cmd % "changed")
      cmdout = rawcmdout.split("\n")
      for line in cmdout:
          if (added_or_updated(line)):
              fname = filename(line)
#	Following restriction is removed since Visual Basic Projects have and need folders
#       like "My Project" and "Web References" for normal usage
#              if (has_space(fname)):
#                sys.stderr.write("File \"%s\" contains whitespace\n" % fname)
#                return 1
#              else:
              if (disallowed_extn(fname)):
                  sys.stderr.write("%s: files of this type not allowed to checkin\n" % fname)
                  return 1

  except:
      f.write("Exception Occurred\n")
      traceback.print_exc(file=sys.stderr)
      return 1

  return 0

if __name__ == "__main__":
# Following code is left commented, in case you need to enable logging.
# Add f.write statements in the code, where ever needed.
#  f = open('/tmp/svn-precommit.log', 'a+')
#  f.write("-- Begin Log at %s --\n" % strftime("%Y-%m-%d %H:%M:%S"))
  exitcode = main()
#  f.write("\n-- End Log at %s --\n" % strftime("%Y-%m-%d %H:%M:%S"))
#  f.close()

  sys.exit(exitcode)

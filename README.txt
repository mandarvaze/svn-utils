Collection of scripts that can be used as hooks in Subversion Repository :

validate-extn.py : 
pre-commit script that ensures developes do not check in .dll, .exe and other intermediate files like .obj
Also checks (currently commented) if the pathname has "white space". Uncomment the code snippet to add this check.

commit-email.py :
You can call this script from post-commit hook as follows :
/usr/share/subversion/hook-scripts/commit-email.py "$REPOS" "$REV" commit-watchers@your.org
This will send out an email with the details of the commit

vsscleanup.py :
This is used to preprocess the VSS data before you start the migration.
It helps remove unwanted files from VSS so that size of data to be processed is reduced.
This will work ONLY on windows (since VSS is supported only on Windows)

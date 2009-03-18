Collection of scripts that can be used as hooks in Subversion Repository :

validate-extn.py : 
pre-commit script that ensures developes do not check in .dll, .exe and other intermediate files like .obj
Also checks (currently commented) if the pathname has "white space". Uncomment the code snippet to add this check.

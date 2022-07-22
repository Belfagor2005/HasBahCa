import os, re, sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")

def upd_done():
	print( "In upd_done")
	xfile ='http://patbuweb.com/HasBahCa/HasBahCa.tar'
	if PY3:
		xfile = b"http://patbuweb.com/HasBahCa/HasBahCa.tar"
	print("Update.py not in PY3")
	fdest = "/tmp/HasBahCa.tar"
	downloadPage(xfile, fdest).addCallback(upd_last)

def upd_last(fplug):
	cmd = "tar -xvf /tmp/HasBahCa.tar -C /"
	print( "cmd A =", cmd)
	os.system(cmd)
	pass


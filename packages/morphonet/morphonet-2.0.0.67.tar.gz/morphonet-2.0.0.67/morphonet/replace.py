# -*- coding: latin-1 -*-
import os,sys
from os.path import isdir,join,isfile

rr=sys.argv[1]
rb=sys.argv[2]


def replace(fn,rr,rb):
	
	if fn.endswith(".py"):
		print(fn)
		fw=open('temp.py','w')
		for line in open(fn,"r"):
			fw.write(line.replace(rr,rb))
		fw.close()
		os.system('cp temp.py '+fn)

plugins="plugins"
for filename in os.listdir(plugins):
	if isfile(join(plugins,filename)):
		replace(join(plugins,filename),rr,rb)

	if isdir(join(plugins,filename)):
		for filename2 in os.listdir(join(plugins,filename)):
			if isfile(join(plugins,filename,filename2)):
				replace(join(plugins,filename,filename2),rr,rb)


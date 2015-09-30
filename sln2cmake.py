import sys
import re
import os.path

def print_usage():
	print 'Usage: sln2cmk.py example.sln'

print '*.sln to CMakeLists.txt converter by Robert Keszeg (c)2015'
print 'Version 0.1 Use without warranty'
	
print "------ Processing command line parameters -----"
if len(sys.argv) < 2:
	print_usage()
	exit()
	
tags =  {"Project":"EndProject",}
slnfilename = sys.argv[1]
i = 0
projects = {}
with open(slnfilename,"r") as slnfile:
	for line in slnfile:
		linearr = line.split('=')
		value = ''
		func = ''
		param = ''
		if len(linearr) > 1:
			value = linearr[1].strip()
			print(linearr[0])
			call = linearr[0].split('(')
			if (len(call) > 1):
				func = call[0].strip()
				param = call[1].strip()
				print func
				if func == 'Project':
					projects[param] = value
			else:
				param = call[0].strip()
		else:
			func = linearr[0].strip()

		i = i+1
		if i>10:
			break
			
for name in projects:
	print 'projects['+name+']='+projects[name]+';'
		




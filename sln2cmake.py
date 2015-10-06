import sys
import re
import os.path
import xml.etree.ElementTree as ET

class Project:
	def __init__(self, name, file, guid):
		self.name = name
		self.file = file
		self.guid = guid
		self.dependencies = []

	def add_dependency(self, otherguid):
		self.dependencies.append(otherguid)

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
projects = []
#stack = []
currentproj = None
currentsection = ''
with open(slnfilename,"r") as slnfile:
	for line in slnfile:

		#setting func, param and value		
		value = ''
		func = ''
		param = ''
		linearr = line.split('=')
		if len(linearr) > 1:
			value = linearr[1].strip()
			call = linearr[0].split('(')
			if (len(call) > 1):
				func = call[0].strip()
				param = call[1].replace(')','').strip()
			else:
				param = call[0].strip()
		else:
			func = linearr[0].strip()

		#processing func, param and value
		if i==0:
			pass
		elif i==1 and func == 'Microsoft Visual Studio Solution File, Format Version 9.00':
			pass
		elif i==2 and func == '# Visual Studio 2005':
			pass
		elif func == 'Project':
			valuearr = value.split(',')
			attrib = {}
			name = valuearr[0]
			attrib['name'] = name
			vcproj = valuearr[1]
			attrib['vcproj'] = vcproj
			guid = valuearr[2]
			attrib['guid'] = guid
			currentproj = Project(name,vcproj,guid)
			projects.append(currentproj)
		elif func == 'EndProject' :
			currentproj = None
		elif func == 'ProjectSection':
			currentsection = param
		elif func == 'EndProjectSection':
			currentsection = ''
#		elif func == 'Global' :
#		elif func == 'EndGlobal' :
#		elif func == 'GlobalSection':
#		elif func == 'EndGlobalSection':
		elif func == '':
			if (currentsection == 'ProjectDependencies'):
				currentproj.add_dependency(param)
		else:
#			print('Error in the sln file line:'+str(i+1)+' <'+func+'>')
			pass

		i = i+1

lines = []
lines.append('cmake_minimum_required(VERSION 3.0)')
lines.append('project('+slnfilename.replace('.sln','')+')')

projnames = {}
for proj in projects:
	guid = proj.guid.replace('"','').strip()
	name = proj.name.strip()
	projnames[guid] = name
	lines.append('include('+name+')')
#	TODO:iterate through .vcprojs with vcproj2cmake.py

for proj in projects:
	if len(proj.dependencies) == 0:
		continue
	lines.append('add_dependencies('+proj.name)
	for dep in proj.dependencies:
		lines.append('\t'+projnames[dep])
	lines.append(')')

cmakefile = open("CMakeLists.txt","w")
cmakefile.write('\n'.join(lines).replace("\t","    "))
cmakefile.close()

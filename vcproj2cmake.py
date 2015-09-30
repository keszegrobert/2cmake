import sys
import os.path
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
projname = root.get("Name")
print "Project name:"+ projname;

print "------ Configurations -----"

targetset = set()
configset = set()
platformset = set()
for config in root.iter("Configuration"):
	cfgarr = config.get("Name").split("|");
	cfgname = '|'.join(cfgarr)
	targetset.add(cfgname)
	configset.add(cfgarr[0])
	platformset.add(cfgarr[1])
	
#	cfgfilename = '_'.join(cfgarr)
#	cfgfilename = cfgfilename.replace(" ","_")
#	print cfgfilename
#	cfgfile = open(cfgfilename+".xml", "w")
#	cfgfile.write(ET.tostring(config))
#	cfgfile.close()

cfg = sorted(list(configset))

def normalizestring(input):
	return input.replace("|","_").replace("(","").replace(")","").replace(" ","_").upper()

targetlist = sorted(list(targetset))
for target in targetlist:
	print normalizestring(target)

class Group:
	def __init__(self,names,files):
		self.names = names
		normalized = []
		for file in files:
			patharr = file.split('\\')
			if patharr[0] == '.':
				newname = '/'.join(patharr[1:])
			else:
				newname = '/'.join(patharr)
			normalized.append(newname)
		self.files = normalized

	def getname(self):
		name = projname+'_'+'_'.join(self.names)+'_SRC'
		return name

	def getnamevar(self):
		name = '${'+self.getname()+'}'
		return name
		
	def tostring(self):
		lines = []
		lines.append('set('+self.getname())
		for file in self.files:
			lines.append('\t'+file)
		lines.append(')')
		
		lines.append('source_group("'+'\\\\'.join(self.names)+'" FILES '+self.getnamevar()+')')
		return '\n'.join(lines)

print "------ Filters -----"
cmake_groups = list()

def getgroupsfor(rootnames,lroot):
#	print "//".join(rootnames)
	files = list()
	for xmlFile in lroot:
		if xmlFile.tag == "Filter":
			continue
		xmlfilename = xmlFile.get("RelativePath")
		if os.path.exists(xmlfilename):
			files.append(xmlfilename)
		else:
			print "file mapped in vcproj not found: " + xmlfilename;
	group = Group(rootnames,files)
	cmake_groups.append(group)
	
	for xmlFilter in lroot:
		if xmlFilter.tag == "File":
			continue
		xmlfiltername = xmlFilter.get("Name")
		newnames = rootnames[:]
		newnames.append(xmlfiltername)
		getgroupsfor(newnames,xmlFilter)
		
xmlFiles = root.find("Files")
getgroupsfor([],xmlFiles)

print "------ Output -----"
lines = []

#lines.append('set(CMAKE_CONFIGURATION_TYPES "'+";".join(cfg)+'" CACHE STRING "VS/XCode configurations" FORCE)')
lines.append('cmake_minimum_required(VERSION 2.8)')
lines.append('project('+projname+')')

for group in cmake_groups:
	lines.append(group.tostring())
	
lines.append('set(SOURCES')
for group in cmake_groups:
	lines.append('\t'+group.getnamevar()+'')
lines.append(')')

lines.append('set(TARGETS')
for target in targetlist:
	lines.append('\t'+target)
for target in targetlist:
	lines.append('\t'+target)
lines.append(')')

lines.append('if (NOT CMAKE_BUILD_TYPE)')
lines.append('set(CMAKE_BUILD_TYPE Debug|Win32 CACHE STRING')
lines.append(' "Choose the type of the build, options are: ${TARGETS} " FORCE)')
lines.append('endif (NOT CMAKE_BUILD_TYPE)')

lines.append('add_library( '+projname+' STATIC ${SOURCES} )')
lines.append('set_target_properties( '+projname+' PROPERTIES LINKER_LANGUAGE C++ )')

print "------ End -----"

cmakefile = open("CMakeLists.txt","w")
cmakefile.write('\n'.join(lines))
cmakefile.close()

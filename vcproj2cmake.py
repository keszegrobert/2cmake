import sys
import xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1])
root = tree.getroot()
print root.tag;
projname = root.get("Name")
print "Project name:"+ projname;

print "------ Configurations -----"
cfgset = set()
for config in root.iter("Configuration"):
	cfgarr = config.get("Name").split("|");
	cfgname = cfgarr[0]
	print cfgname
	cfgset.add(cfgname)

cfg = sorted(list(cfgset))
print "------ Filters -----"
cmake_groups = list()

class Group:
	def __init__(self,names,files):
		self.names = names
		normalized = []
		for file in files:
			patharr = file.split('\\')[1:]
			newname = '/'.join(patharr)
			normalized.append(newname)
		self.files = normalized
		
	def tostring(self):
		name = projname+'_'+'_'.join(self.names)+'_SRC'
		setting = '\nset('+name+'\n\t'+'\n\t'.join(self.files)+'\n)\n'
		group ='source_group("'+'\\\\'.join(self.names)+'" FILES ${'+name+'})\n'
		return setting + group
		
def getgroupsfor(rootnames,lroot):
	print "//".join(rootnames)
	files = list()
	for xmlFile in lroot:
		if xmlFile.tag == "Filter":
			continue
		xmlfilename = xmlFile.get("RelativePath")
		files.append(xmlfilename)
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
cmakefile = open("CMakeLists.txt","w")
	
cmakefile.write('set(CMAKE_CONFIGURATION_TYPES "'+";".join(cfg)+'" CACHE STRING "VS/XCode configurations" FORCE)\n')
cmakefile.write('cmake_minimum_required(VERSION 2.8)\n');
cmakefile.write('project('+projname+')\n')

for group in cmake_groups:
	cmakefile.write(group.tostring())
print "------ End -----"

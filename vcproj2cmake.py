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
#for target in targetlist:
#	print normalizestring(target)

class Config:
	def __init__(self, name, properties):
		self.name = name
		self.properties = properties.copy()
		self.tools = {}
		self.files = list()
		
	def add_tool(self,name,properties):
		self.tools[name] = properties
		
	def add_file(self,file):
		self.files.append(file)
		
	def get_string(self):
		lines = list()
		lines.append('if(CMAKE_BUILD_TYPE STREQUAL "'+self.name+'")')
		#include directories
		if self.tools.has_key('VCCLCompilerTool'):
			tool = self.tools['VCCLCompilerTool']
			if tool.has_key('AdditionalIncludeDirectories'):
				includes = tool['AdditionalIncludeDirectories'].split(';')
				lines.append('\tinclude_directories(')
				for dir in includes:
					lines.append('\t\t'+dir)
				lines.append('\t)')
			
		#source files
		lines.append('')
		lines.append('\tset(CONFIGSRC ')
		for file in self.files:
			lines.append('\t\t'+file)
		lines.append('\t)')

		#goal target
		lines.append('#')
		type = self.properties['ConfigurationType']
		if type == '1':
			lines.append('\tadd_executable('+projname+' ${CONFIGSRC})')
		elif type == '2':
			lines.append('\tadd_library('+projname+' SHARED ${CONFIGSRC})')
		elif type == '4':
			lines.append('\tadd_library('+projname+' STATIC ${CONFIGSRC})')
		else:
			print 'Unknown configuration type:'+type
			
		lines.append('endif()')
		return lines
	
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
		
		lines.append('source_group("'+'\\\\'.join(self.names)+'"')
		lines.append('\tFILES '+self.getnamevar())
		lines.append(')')
		return lines

print "------ Filters -----"
cmake_groups = list()
vcproj_configs = {}

def readconfigs(lroot):
	for configxml in lroot:
		cfgname = configxml.get("Name")
		cfgprops = configxml.attrib
		cfg = Config(cfgname,cfgprops)
		for toolxml in configxml:
			toolprops = toolxml.attrib
			toolname = toolxml.get('Name')
			cfg.add_tool(toolname,toolprops)
		vcproj_configs[cfgname] = cfg

def readfileconfigs(fname,lroot):
	for fileConfig in lroot:
		cname = fileConfig.get('Name')
		excluded = False
		if ( fileConfig.attrib.has_key('ExcludedFromBuild')) and (fileConfig.get('ExcludedFromBuild') == "true"):
			excluded = True
#			print "Excluded:"+fname
		
		config = vcproj_configs[cname]
		for tool in fileConfig:
			if not excluded:
				config.add_file(fname)

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
		readfileconfigs(xmlfilename,xmlFile)
	group = Group(rootnames,files)
	cmake_groups.append(group)
	
	for xmlFilter in lroot:
		if xmlFilter.tag == "File":
			continue
		xmlfiltername = xmlFilter.get("Name")
		newnames = rootnames[:]
		newnames.append(xmlfiltername)
		getgroupsfor(newnames,xmlFilter)
		
xmlConfigs = root.find("Configurations")
readconfigs(xmlConfigs)

xmlFiles = root.find("Files")
getgroupsfor([],xmlFiles)

print "------ Output -----"
lines = []

#lines.append('set(CMAKE_CONFIGURATION_TYPES "'+";".join(cfg)+'" CACHE STRING "VS/XCode configurations" FORCE)')
lines.append('cmake_minimum_required(VERSION 2.8)')
lines.append('project('+projname+')')

for group in cmake_groups:
	lines.extend(group.tostring())
	
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

lines.append('if(NOT CMAKE_BUILD_TYPE)')
lines.append('set(CMAKE_BUILD_TYPE Debug|Win32 CACHE STRING')
lines.append('\t"Choose the type of the build, options are: ${TARGETS} " FORCE)')
lines.append('endif()')

lines.append('add_library( '+projname+' STATIC ${SOURCES} )')
lines.append('set_target_properties( '+projname+' PROPERTIES LINKER_LANGUAGE C++ )')

for name in vcproj_configs:
	lines.extend(vcproj_configs[name].get_string())
	
print "------ End -----"

cmakefile = open("CMakeLists.txt","w")
cmakefile.write('\n'.join(lines).replace("\t","    "))
cmakefile.close()

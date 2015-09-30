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

def normalizepath(input):
	patharr = input.split('\\')
	if patharr[0] == '.':
		newname = '/'.join(patharr[1:])
	else:
		newname = '/'.join(patharr)
	return newname
	
targetlist = sorted(list(targetset))

custom_commands = {}
#for target in targetlist:
#	print normalizestring(target)

class Command:
	def __init__(self,name,command,extension,output,description):
		self.name = name
		self.command = command
		self.extension = extension
		self.output = output
		self.description = description
	def getstrings(self):
		lines = list()
		lines.append('add_custom_target("'+self.name+'"')
		lines.append('\tOUTPUT "'+normalizepath(self.output)+'"')
		lines.append('\tCOMMAND \''+normalizepath(self.command)+'\'')
		lines.append('\tCOMMENT "'+self.description+'"')
		lines.append('\tSOURCES ${SOURCES}')
		lines.append(')')
		return lines

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
					lines.append('\t\t'+dir.replace("\\","/"))
				lines.append('\t)')
			
		#source files
		lines.append('')
		lines.append('\tlist(APPEND CONFIGSRC ')
		for file in self.files:
			lines.append('\t\t"'+normalizepath(file)+'"')
		lines.append('\t)')
		
		for cmd in custom_commands:
			command = custom_commands[cmd];
			#lines.extend(command.getstrings())

		#goal target
		lines.append('#')
		type = self.properties['ConfigurationType']
		if type == '1':
			lines.append('\tadd_executable('+projname+' ${SOURCES})')
		elif type == '2':
			lines.append('\tadd_library('+projname+' SHARED ${SOURCES})')
		elif type == '4':
			lines.append('\tadd_library('+projname+' STATIC ${SOURCES})')
		else:
			print 'Unknown configuration type:'+type
			
		lines.append('endif()')
		return lines

class Group:
	def __init__(self,names,files):
		self.names = names
		normalized = []
		for file in files:
			newname = normalizepath(file)
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
			lines.append('\t"'+file+'"')
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
		
def getTool(toolpath):
	xmltool = ET.parse(toolpath)
	root = xmltool.getroot()
	print "TOOL: "+root.get("Name")
	xmlrules = xmltool.find("Rules")
	for xmlbuildrule in xmlrules:
		name = xmlbuildrule.get("Name")
		cmd = xmlbuildrule.get("CommandLine")
		ext = xmlbuildrule.get("FileExtensions")
		output = xmlbuildrule.get("Outputs")
		description = xmlbuildrule.get("ExecutionDescription");
		custom_commands[name] = Command(name,cmd,ext,output,description)
		
xmlTools = root.find("ToolFiles")
for xmlTool in xmlTools:
	getTool(xmlTool.get("RelativePath"))
	
xmlConfigs = root.find("Configurations")
readconfigs(xmlConfigs)

xmlFiles = root.find("Files")
getgroupsfor([],xmlFiles)

print "------ Output -----"
lines = []

#lines.append('set(CMAKE_CONFIGURATION_TYPES "'+";".join(cfg)+'" CACHE STRING "VS/XCode configurations" FORCE)')
lines.append('cmake_minimum_required(VERSION 2.8)')
lines.append('project('+projname+')')
lines.append('set(CONFIGSRC)')
lines.append('if(NOT CMAKE_BUILD_TYPE)')
lines.append('set(CMAKE_BUILD_TYPE Debug|Win32 CACHE STRING')
lines.append('\t"Choose the type of the build, options are: ${TARGETS} " FORCE)')
lines.append('endif()')

for group in cmake_groups:
	lines.extend(group.tostring())
	
lines.append('set(SOURCES')
for group in cmake_groups:
	lines.append('\t'+group.getnamevar()+'')
lines.append(')')

lines.append('set(TARGETS')
for target in targetlist:
	lines.append('\t"'+target+'"')
lines.append(')')

for name in vcproj_configs:
	lines.extend(vcproj_configs[name].get_string())
	
lines.append('set_target_properties( '+projname+' PROPERTIES LINKER_LANGUAGE C++ )')

	
lines.append('set(TOEXCLUDE ${SOURCES})')
lines.append('list(REMOVE_ITEM TOEXCLUDE ${CONFIGSRC})')
lines.append('set_source_files_properties(${TOEXCLUDE} PROPERTIES HEADER_FILE_ONLY ON)')

print "------ End -----"

cmakefile = open("CMakeLists.txt","w")
cmakefile.write('\n'.join(lines).replace("\t","    "))
cmakefile.close()

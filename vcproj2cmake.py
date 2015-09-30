import sys
import os.path
import xml.etree.ElementTree as ET
	
flaglist = []
#VC7
flaglist.append({'name':'BasicRuntimeChecks', 'flag':'/GZ', 'value':'1'})
flaglist.append({'name':'BasicRuntimeChecks', 'flag':'/RTCsu', 'value':'3'})
flaglist.append({'name':'BasicRuntimeChecks', 'flag':'/RTCs', 'value':'1'})
flaglist.append({'name':'BasicRuntimeChecks', 'flag':'/RTCu', 'value':'2'})
flaglist.append({'name':'BasicRuntimeChecks', 'flag':'/RTC1', 'value':'3'})
flaglist.append({'name':'DebugInformationFormat', 'flag':'/Z7', 'value':'1'})
flaglist.append({'name':'DebugInformationFormat', 'flag':'/Zd', 'value':'2'})
flaglist.append({'name':'DebugInformationFormat', 'flag':'/Zi', 'value':'3'})
flaglist.append({'name':'DebugInformationFormat', 'flag':'/ZI', 'value':'4'})
flaglist.append({'name':'EnableEnhancedInstructionSet', 'flag':'/arch:SSE2', 'value':'2'})
flaglist.append({'name':'EnableEnhancedInstructionSet', 'flag':'/arch:SSE', 'value':'1'})
flaglist.append({'name':'FloatingPointModel', 'flag':'/fp:precise', 'value':'0'})
flaglist.append({'name':'FloatingPointModel', 'flag':'/fp:strict', 'value':'1'})
flaglist.append({'name':'FloatingPointModel', 'flag':'/fp:fast', 'value':'2'})
flaglist.append({'name':'FavorSizeOrSpeed', 'flag':'/Ot',  'value':'1'})
flaglist.append({'name':'FavorSizeOrSpeed', 'flag':'/Os', 'value':'2'})
flaglist.append({'name':'CompileAs', 'flag':'/TC','value':'1'})
flaglist.append({'name':'CompileAs', 'flag':'/TP','value':'2'})
flaglist.append({'name':'Optimization', 'flag':'/Od','value':'0'})
flaglist.append({'name':'Optimization', 'flag':'/O1','value':'1'})
flaglist.append({'name':'Optimization', 'flag':'/O2','value':'2'})
flaglist.append({'name':'Optimization', 'flag':'/Ox', 'value':'3'})
flaglist.append({'name':'OptimizeForProcessor', 'flag':'/GB', 'value':'0'})
flaglist.append({'name':'OptimizeForProcessor', 'flag':'/G5','value':'1'})
flaglist.append({'name':'OptimizeForProcessor', 'flag':'/G6','value':'2'})
flaglist.append({'name':'OptimizeForProcessor', 'flag':'/G7','value':'3'})
flaglist.append({'name':'InlineFunctionExpansion', 'flag':'/Ob0','value':'0'})
flaglist.append({'name':'InlineFunctionExpansion', 'flag':'/Ob1','value':'1'})
flaglist.append({'name':'InlineFunctionExpansion', 'flag':'/Ob2', 'value':'2'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/MTd','value':'1'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/MT', 'value':'0'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/MDd', 'value':'3'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/MD','value':'2'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/MLd','value':'5'})
flaglist.append({'name':'RuntimeLibrary', 'flag':'/ML','value':'4'})
flaglist.append({'name':'StructMemberAlignment', 'flag':'/Zp16','value':'5'})
flaglist.append({'name':'StructMemberAlignment', 'flag':'/Zp1','value':'1'})
flaglist.append({'name':'StructMemberAlignment', 'flag':'/Zp2','value':'2'})
flaglist.append({'name':'StructMemberAlignment', 'flag':'/Zp4','value':'3'})
flaglist.append({'name':'StructMemberAlignment', 'flag':'/Zp8','value':'4'})
flaglist.append({'name':'WarningLevel', 'flag':'/W0', 'value':'0'})
flaglist.append({'name':'WarningLevel', 'flag':'/W1', 'value':'1'})
flaglist.append({'name':'WarningLevel', 'flag':'/W2', 'value':'2'})
flaglist.append({'name':'WarningLevel', 'flag':'/W3', 'value':'3'})
flaglist.append({'name':'WarningLevel', 'flag':'/W4', 'value':'4'})
flaglist.append({'name':'BufferSecurityCheck', 'flag':'/GS-', 'value':'false'})
flaglist.append({'name':'BufferSecurityCheck', 'flag':'/GS', 'value':'true'})
flaglist.append({'name':'Detect64BitPortabilityProblems', 'flag':'/Wp64','value':'true'})
flaglist.append({'name':'EnableFiberSafeOptimizations', 'flag':'/GT','value':'true'})
flaglist.append({'name':'EnableFunctionLevelLinking', 'flag':'/Gy','value':'true'})
flaglist.append({'name':'EnableIntrinsicFunctions', 'flag':'/Oi', 'value':'true'})
flaglist.append({'name':'GlobalOptimizations', 'flag':'/Og', 'value':'true'})
flaglist.append({'name':'ImproveFloatingPointConsistency', 'flag':'/Op', 'value':'true'})
flaglist.append({'name':'MinimalRebuild', 'flag':'/Gm', 'value':'true'})
flaglist.append({'name':'OmitFramePointers', 'flag':'/Oy', 'value':'true'})
flaglist.append({'name':'OptimizeForWindowsApplication', 'flag':'/GA', 'value':'true'})
flaglist.append({'name':'RuntimeTypeInfo', 'flag':'/GR', 'value':'true'})
flaglist.append({'name':'RuntimeTypeInfo', 'flag':'/GR-','value':'false'})
flaglist.append({'name':'SmallerTypeCheck', 'flag':'/RTCc', 'value':'true'})
flaglist.append({'name':'SuppressStartupBanner', 'flag':'/nologo', 'value':'true'})
flaglist.append({'name':'WholeProgramOptimization', 'flag':'/GL', 'value':'true'})
flaglist.append({'name':'WholeProgramOptimization', 'flag':'/GL-','value':'false'})
flaglist.append({'name':'WarnAsError', 'flag':'/WX', 'value':'true'})
flaglist.append({'name':'BrowseInformation', 'flag':'/FR', 'value':'1'})
flaglist.append({'name':'StringPooling', 'flag':'/GF', 'value':'true'})
flaglist.append({'name':'ShowIncludes', 'flag':'/showIncludes', 'value':'true'})
#VC8  
flaglist.append({'name':'CallingConvention', 'flag':'/Gd', 'value':'0'})
flaglist.append({'name':'CallingConvention', 'flag':'/Gr', 'value':'1'})
flaglist.append({'name':'CallingConvention', 'flag':'/Gz', 'value':'2'})
flaglist.append({'name':'ErrorReporting', 'flag':'/errorReport:prompt', 'value':'1'})
flaglist.append({'name':'ErrorReporting', 'flag':'/errorReport:queue', 'value':'2'})
flaglist.append({'name':'ExceptionHandling', 'flag':'/GX', 'value':'1'})
flaglist.append({'name':'ExceptionHandling', 'flag':'/EHsc', 'value':'1'})
flaglist.append({'name':'ExceptionHandling', 'flag':'/EHa', 'value':'2'})
flaglist.append({'name':'EnablePREfast', 'flag':'/analyze', 'value':'true'})
flaglist.append({'name':'EnablePREfast', 'flag':'/analyze-', 'value':'false'})
flaglist.append({'name':'TreatWChar_tAsBuiltInType', 'flag':'/Zc:wchar_t', 'value':'true'})
flaglist.append({'name':'TreatWChar_tAsBuiltInType', 'flag':'/Zc:wchar_t-', 'value':'false'})

def print_usage():
	print 'Usage: vc2cm.py example.vcproj [-m foo=bar]* '
	print 'Available commands:'
	print "\t-m\tdefine macros"

print '*.vcproj to CMakeLists.txt converter /by Robert Keszeg (c)2015'
print 'Version 0.8 Use without warranty'
	
print "------ Processing command line parameters -----"
if len(sys.argv) < 2:
	print_usage()
tree = ET.parse(sys.argv[1])
root = tree.getroot()
projname = root.get("Name")
print "Project name:"+ projname;

commands = sys.argv[2:len(sys.argv)]
state = 'free'
macros = {}

for command in commands:
	print 'command:'+command
	if (state == 'free'):
		if command == '-m':
			state = 'macro'
		else:
			print 'Error: I don\'t understand the command<'+command+'>'
			print_usage()
	elif (state == 'macro'):
		marr = command.split('=')
		macros[marr[0]] = marr[1]
#		print '$('+marr[0]+') = "'+marr[1]+'"'
		state = 'free'

def normalizepath(input):
	patharr = input.split('\\')
	if patharr[0] == '.':
		newname = '/'.join(patharr[1:])
	else:
		newname = '/'.join(patharr)
	for key in macros:
		newname = newname.replace('$('+key+')',macros[key])
#	print 'NORMALIZING:'+input+'==>'+newname
	return newname

def pack_flag(flag,filename):
	return flag+'\\"'+normalizepath(filename)+'\\"'

		
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

def get_compile_flags(tool):
	compile_flags = []
	if tool.has_key('AdditionalOptions'):
		compile_flags.extend(tool['AdditionalOptions'].split(';'))
	for item in flaglist:
		if tool.has_key(item['name']):
			if tool[item['name']] == item['value']:
				compile_flags.append(item['flag'])
				
	if tool.has_key('DisableSpecificWarnings'):
		warnings = tool['DisableSpecificWarnings']
		warning_list = warnings.split(';')
		for warning in warning_list:
			compile_flags.append('/wd'+warning)
		
#	if tool.has_key('UsePrecompiledHeader') and tool['UsePrecompiledHeader'] != '0':
#		headerthrough = 'stdafx.h'
#		if tool.has_key('PrecompiledHeaderThrough'):
#			headerthrough = tool['PrecompiledHeaderThrough']
#		if tool['UsePrecompiledHeader'] == '1':
#			compile_flags.append(pack_flag('/Yc',headerthrough))
#		if tool['UsePrecompiledHeader'] == '2':
#			compile_flags.append(pack_flag('/Yu',headerthrough))
#			
#		header = '$(IntDir)\$(TargetName).pch'
#		if tool.has_key('PrecompiledHeaderFile'):
#			header = tool['PrecompiledHeaderFile']
#		compile_flags.append(pack_flag('/Fp',header))
		
	if tool.has_key('ForcedIncludeFiles'):
		compile_flags.append(pack_flag('/FI',tool['ForcedIncludeFiles']))

	if tool.has_key('ForcedUsingFiles'):
		compile_flags.append(pack_flag('/FU',tool['ForcedUsingFiles']))

	if tool.has_key('UndefinePreprocessorDefinitions'):
		compile_flags.append(pack_flag('/U',tool['UndefinePreprocessorDefinitions']))

	if tool.has_key('AssemblerListingLocation'):
		compile_flags.append(pack_flag('/Fa',tool['AssemblerListingLocation']))
		
	if tool.has_key('ProgramDataBaseFileName'):
		compile_flags.append(pack_flag('/Fd',tool['ProgramDataBaseFileName']))

	return compile_flags
	
	
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
					lines.append('\t\t'+normalizepath(dir))
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
		
		if self.tools.has_key('VCCLCompilerTool'):
			tool = self.tools['VCCLCompilerTool']
			if tool.has_key('PreprocessorDefinitions'):
				preprocessor = tool['PreprocessorDefinitions'].split(';')
				lines.append('\tset_property(TARGET '+projname);
				lines.append('\t\tAPPEND PROPERTY COMPILE_DEFINITIONS');
				for prep in preprocessor:
					lines.append('\t\t'+prep);
				lines.append('\t)')
			
			#additional options
			compile_flags = get_compile_flags(tool)
			if len(compile_flags):
				lines.append('\tif(MSVC)')
				for compile_flag in compile_flags:
					lines.append('\t\tset_property(TARGET '+projname+' APPEND_STRING PROPERTY COMPILE_FLAGS')
					lines.append('\t\t\t"'+compile_flag+' "')#notice the extra space after every flag
					lines.append('\t\t)')
				lines.append('\tendif()')

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
		
		if vcproj_configs.has_key(cname):
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

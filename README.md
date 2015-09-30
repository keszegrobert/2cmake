# 2cmake
Python tools able to generate CMakelists.txt from various sources

#vcproj2cmake.py

This converter is able to generate CMakeLists.txt from a vcproj file

- source_group from the <Filter> tags
- excluded files support
- processing <Configuration> tags
- COMPILE_FLAGS from VCCLCompilerTool <Tool> 
- Preprocessor definitions

#sln2cmake

- only prints out the found Projects

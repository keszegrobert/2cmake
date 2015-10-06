# 2cmake
Python tools able to generate CMakelists.txt from various sources

#vcproj2cmake.py

This converter is able to generate CMakeLists.txt from a vcproj file

- source_group from the &lt;Filter&gt; tags
- excluded files support
- processing &lt;Configuration&gt; tags
- COMPILE_FLAGS from VCCLCompilerTool &lt;Tool&gt;
- Preprocessor definitions

#sln2cmake

- processes the project dependencies and creates a CMakelists.txt for them

TODO:
- generate linker flags
- refactor the code
- custom build tools to cmake custom command

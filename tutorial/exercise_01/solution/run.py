# Import Python modules
from vunit import VUnit
from os.path import join, dirname

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = dirname(__file__)

# Add VHDL libraries to project
lib = prj.add_library("lib")
tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to libraries
lib.add_source_files(join(root, "src", "*.vhd"))
tb_lib.add_source_files(join(root, "test", "*.vhd"))

# Run VUnit
prj.main()

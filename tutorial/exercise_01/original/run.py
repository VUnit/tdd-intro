# Import Python modules
from vunit import VUnit
from os.path import join, dirname

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = dirname(__file__)

# Add VHDL libraries to project
lib = prj.add_library("lib")

# Add all VHDL files to libraries
lib.add_source_files(join(root, "src", "*.vhd"))

# Run VUnit
prj.main()

# Import Python modules
from vunit import VUnit
from os.path import join, dirname

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = dirname(__file__)

# Add VHDL libraries to project
# add_external_library(library_name, path: Union[str, pathlib.Path], vhdl_standard: Optional[str] = None)
lib = prj.add_external_library("lib", join(root, "..", "exercise_01", "vunit_out", "modelsim", "libraries", "lib"))
tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to libraries
tb_lib.add_source_files(join(root, "test", "*.vhd"))

# Set simulator specific compile options
prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Set generic for all testbenches and test cases
#prj.set_generic("width", 16);

# Run VUnit
prj.main()

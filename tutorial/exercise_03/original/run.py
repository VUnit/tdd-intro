# Import Python modules
from pathlib import Path
from vunit import VUnit

# Setup Python test runner project from command line arguments
PRJ = VUnit.from_argv()

# Set the root to the directory of this script file
ROOT = Path(__file__).resolve().parent

# Add external VHDL libraries to project
for simulator in ["modelsim", "ghdl", "rivierapro", "activehdl"]:
    if simulator_is(simulator):
        PRJ.add_external_library("lib", ROOT.parent.parent / "exercise_01/solution/vunit_out" / simulator / "libraries/lib")
        break

# Create and add a regular library and add all VHDL files to it
TB_LIB = PRJ.add_library("tb_lib")
TB_LIB.add_source_files(ROOT / "test" / "*.vhd")
# or PRJ.add_library("tb_lib").add_source_files(join(root, "test", "*.vhd"))

# Set simulator specific compile options
if simulator_is("rivierapro"):
    PRJ.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Set generic for all testbenches and test cases
#PRJ.set_generic("width", 16);

# Run VUnit
PRJ.main()

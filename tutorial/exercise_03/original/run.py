"""Run script for exercise_03."""

# Import Python modules
from pathlib import Path
from vunit import VUnit
from vunit.sim_if.common import simulator_is

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = Path(__file__).resolve().parent

# Add external VHDL libraries to project
for simulator in ["modelsim", "ghdl", "rivierapro", "activehdl"]:
    if simulator_is(simulator):
        prj.add_external_library(
            "lib", root.parent.parent / "exercise_01/solution/vunit_out" / simulator / "libraries/lib"
        )
        break

# Create and add a regular library and add all VHDL files to it
tb_lib = prj.add_library("tb_lib")
tb_lib.add_source_files(root / "test" / "*.vhd")
# or prj.add_library("tb_lib").add_source_files(join(root, "test", "*.vhd"))

# Set simulator specific compile options
if simulator_is("rivierapro"):
    prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Set generic for all testbenches and test cases
# prj.set_generic("width", 16);

# Run VUnit
prj.main()

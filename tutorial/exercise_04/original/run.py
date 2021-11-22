"""Run script for exercise_04."""

# Import Python modules
from pathlib import Path
from vunit import VUnit

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Enable location for logs
# prj.enable_location_preprocessing()

# Set the root to the directory of this script file
root = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to Libraries
tb_lib.add_source_files(root / "test" / "*.vhd")

# Set simulator specific compile options
prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
prj.main()

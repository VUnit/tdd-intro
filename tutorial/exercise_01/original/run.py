"""Run script for exercise_01."""

# Import Python modules
from pathlib import Path
from vunit import VUnit

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
lib = prj.add_library("lib")

# Add all VHDL files to Libraries
lib.add_source_files(root / "src" / "*.vhd")

# Run VUnit
prj.main()

# Import Python modules
from vunit import VUnit
from pathlib import Path

# Setup Python test runner project from command line arguments
PRJ = VUnit.from_argv()

# Set the root to the directory of this script file
ROOT = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
LIB = PRJ.add_library("lib")
TB_LIB = PRJ.add_library("tb_lib")

# Add all VHDL files to Libraries
LIB.add_source_files(ROOT / "src" / "*.vhd")
TB_LIB.add_source_files(ROOT / "test" / "*.vhd")

# Run VUnit
PRJ.main()

# Import Python modules
from vunit import VUnit
from pathlib import Path

# Setup Python test runner project from command line arguments
PRJ = VUnit.from_argv()

# Set the root to the directory of this script file
ROOT = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
COMMON_LIB = PRJ.add_library("common_lib")
TB_LIB = PRJ.add_library("tb_lib")

# Add all VHDL files to libraries
COMMON_LIB.add_source_files(ROOT.parent.parent/ "common"/ "src"/ "*.vhd")
TB_LIB.add_source_files(ROOT/ "test"/ "*.vhd")

# Set simulator specific compile options
PRJ.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
PRJ.main()
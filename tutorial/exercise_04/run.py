# Import Python modules
from vunit import VUnit
from pathlib import Path

# Setup Python test runner project from command line arguments
PRJ = VUnit.from_argv()

# Enable location for logs
#prj.enable_location_preprocessing()

# Set the root to the directory of this script file
ROOT = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
TB_LIB = PRJ.add_library("tb_lib")

# Add all VHDL files to Libraries
TB_LIB.add_source_files(ROOT / "test" / "*.vhd")

# Set simulator specific compile options
PRJ.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
PRJ.main()

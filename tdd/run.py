"""VUnit run script."""

from pathlib import Path
from vunit import VUnit

prj = VUnit.from_argv()
lib = prj.add_library("lib")

root = Path(__file__).parent
lib.add_source_files(root / "src" / "*.vhd")
lib.add_source_files(root / "test" / "*.vhd")

prj.main()

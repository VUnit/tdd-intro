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

# Set simulator specific compile options
if simulator_is("rivierapro"):
    prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Set generic for all testbenches and test cases
prj.set_generic("width", 16)

# Get the tb_counter_with_test_cases testbench (= entity) from the tb_lib library in which it has been compiled
tb_counter_with_test_cases = tb_lib.entity("tb_counter_with_test_cases")

# Add a named configuration for tb_counter_with_test_cases with the width generic set to 12
tb_counter_with_test_cases.add_config(name="width=12", generics=dict(width=12))

# Get the "Test counting" test case from the tb_counter_with_test_cases testbench
test_counting = tb_counter_with_test_cases.test("Test counting")

# Add named configurations for the "Test counting" test case with the width generic set to 32, 64, and 128
for value in [32, 64, 128]:
    test_counting.add_config(name=f"width={value}", generics=dict(width=value))

# Run VUnit
prj.main()

# Import Python modules
from vunit import VUnit
from os.path import join, dirname
from vunit.sim_if.common import simulator_is

# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = dirname(__file__)

# Add VHDL libraries to project
for simulator in ["modelsim", "ghdl", "rivierapro", "activehdl"]:
    if simulator_is(simulator):
        lib = prj.add_external_library("lib", join(root, "..", "..", "exercise_01", "solution", "vunit_out", simulator, "libraries", "lib"))
        break

tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to libraries
tb_lib.add_source_files(join(root, "test", "*.vhd"))

# Set simulator specific compile options
prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Set generic for all testbenches and test cases
prj.set_generic("width", 16);

# Get the tb_counter_with_test_cases testbench (= entity) from the tb_lib library in which it has been compiled
tb_counter_with_test_cases = tb_lib.entity("tb_counter_with_test_cases")

# Add a named configuration for tb_counter_with_test_cases with the width generic set to 12
tb_counter_with_test_cases.add_config(name="width=12", generics=dict(width=12))

# Get the "Test counting" test case from the tb_counter_with_test_cases testbench
test_counting = tb_counter_with_test_cases.test("Test counting")

# Add named configurations for the "Test counting" test case with the width generic set to 32, 64, and 128
for value in [32, 64, 128]:
    test_counting.add_config(name="width=%s" % value, generics=dict(width=value))

# Run VUnit
prj.main()

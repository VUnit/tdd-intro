# Import Python modules
from vunit import VUnit
from os.path import join, dirname
import csv
from itertools import zip_longest
from random import sample

def function_running_before_test_case(output_path):
    """
    This function generates input to the test case.
    """
    # Write som random values
    with open(join(output_path, "python_data.csv"), "w", newline="") as python_data_file:
        python_data = csv.writer(python_data_file, delimiter=',')
        python_data.writerow(sample(range(0, 2**16), 25))

    # Must return True or the test case will fail
    return True

def function_running_after_test_case(output_path):
    """
    This function verifies the output from the test case.
    """
    with open(join(output_path, "python_data.csv")) as python_data_file, open(join(output_path, "dut_response.csv")) as dut_response_file:
        python_data = csv.reader(python_data_file, delimiter=',')
        dut_response = csv.reader(dut_response_file, delimiter=',')

        for a, b in zip_longest(python_data, dut_response):
            expected = list(map(lambda x:int(x) + 1, a))
            got = list(map(int, b))
            if got != expected:
                print("Got %s, expected %s" % (str(got), str(expected)))
                return False

        return True


# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Set the root to the directory of this script file
root = dirname(__file__)

# Add VHDL libraries to project
common_lib = prj.add_library("common_lib")
tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to libraries
common_lib.add_source_files(join(root, "..", "common", "src", "*.vhd"))
tb_lib.add_source_files(join(root, "test", "*.vhd"))

# Add configuration to generate and verify data in Python hooks
tb_lib.test_bench("tb_file_based_testing").test("Test generating and verifying data in hooks").add_config(
    name="hooks demo",
    pre_config=function_running_before_test_case,
    post_check=function_running_after_test_case)

# Set simulator specific compile options
prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
prj.main()

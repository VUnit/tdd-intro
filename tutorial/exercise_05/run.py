# Import Python modules
from vunit import VUnit
from pathlib import Path
import csv
from itertools import zip_longest
from random import sample

def function_running_before_test_case(output_path):
    """
    This function generates input to the test case.
    """
    # Write som random values
    with open(output_path+ "/python_data.csv", "w", newline="") as python_data_file:
        python_data = csv.writer(python_data_file, delimiter=',')
        python_data.writerow(sample(range(0, 2**16), 25))

    # Must return True or the test case will fail
    return True

def function_running_after_test_case(output_path):
    """
    This function verifies the output from the test case.
    """
    with open(output_path+ "/python_data.csv") as python_data_file, open(output_path+ "/dut_response.csv") as dut_response_file:
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
PRJ = VUnit.from_argv()

# Set the root to the directory of this script file
ROOT = Path(__file__).resolve().parent

# Create and add VHDL Libraries to project
COMMON_LIB = PRJ.add_library("common_lib")
TB_LIB = PRJ.add_library("tb_lib")

# Add all VHDL files to libraries
COMMON_LIB.add_source_files(ROOT.parent/ "common"/ "src"/ "*.vhd")
TB_LIB.add_source_files(ROOT/ "test"/ "*.vhd")

# Add configuration to generate and verify data in Python hooks
TB_LIB.test_bench("tb_file_based_testing").test("Test generating and verifying data in hooks").add_config(
    name="hooks demo",
    pre_config=function_running_before_test_case,
    post_check=function_running_after_test_case)

# Set simulator specific compile options
PRJ.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
PRJ.main()
"""Run script for exercise_05."""

# Import Python modules
from pathlib import Path
import csv
from itertools import zip_longest
from random import sample
from subprocess import run
from vunit import VUnit

# Set the root to the directory of this script file
root = Path(__file__).resolve().parent


def function_running_before_test_case(output_path):
    """Generate input to the test case."""
    # Write some random values
    with open(Path(output_path) / "python_data.csv", "w", newline="", encoding="utf-8") as python_data_file:
        python_data = csv.writer(python_data_file, delimiter=",")
        python_data.writerow(sample(range(0, 2 ** 16), 25))

    # Must return True or the test case will fail
    return True


def function_running_after_test_case(output_path):
    """Verify the output from the test case."""
    with open(Path(output_path) / "python_data.csv", encoding="utf-8") as python_data_file, open(
        Path(output_path) / "dut_response.csv", encoding="utf-8"
    ) as dut_response_file:
        python_data = csv.reader(python_data_file, delimiter=",")
        dut_response = csv.reader(dut_response_file, delimiter=",")

        for stimuli, result in zip_longest(python_data, dut_response):
            expected = list(map(lambda x: int(x) + 1, stimuli))
            got = list(map(int, result))
            if got != expected:
                print(f"Got {got}, expected {expected}")
                return False

        return True


def generate_stimuli(output_path):
    """Call Octave to generate stimuli to the simulation."""
    proc = run(
        [
            "octave-cli",
            root / "octave" / "generate_stimuli.m",
            Path(output_path),
        ],
        cwd=root,
        check=False,
    )

    return proc.returncode == 0


def verify_output(output_path):
    """Call Octave to verify the output from the simulation."""
    proc = run(
        [
            "octave-cli",
            root / "octave" / "verify_output.m",
            Path(output_path) / "stimuli.csv",
            Path(output_path) / "dut_response.csv",
        ],
        cwd=root,
        check=False,
    )

    return proc.returncode == 0


# Setup Python test runner project from command line arguments
prj = VUnit.from_argv()

# Create and add VHDL Libraries to project
common_lib = prj.add_library("common_lib")
tb_lib = prj.add_library("tb_lib")

# Add all VHDL files to libraries
common_lib.add_source_files(root.parent.parent / "common" / "src" / "*.vhd")
tb_lib.add_source_files(root / "test" / "*.vhd")

# Add configuration to generate and verify data in Python hooks
test = tb_lib.test_bench("tb_file_based_testing").test("Test generating and verifying data in hooks")
test.add_config(
    name="hooks demo",
    pre_config=function_running_before_test_case,
    post_check=function_running_after_test_case,
)

# Add hooks to generate and verify data with Matlab/Octave. If there is only one configuration
# you can also set the pre_config and post_check functions directly
test = tb_lib.test_bench("tb_file_based_testing").test("Test Matlab/Octave co-simulation")
test.set_pre_config(generate_stimuli)
test.set_post_check(verify_output)

# Set simulator specific compile options
prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])

# Run VUnit
prj.main()

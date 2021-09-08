import unittest
import sys
from sys import executable
from os import environ
from pathlib import Path
from subprocess import call
from tests.common import check_report
from vunit.sim_if.common import has_simulator


ROOT = Path(__file__).resolve().parent


@unittest.skipUnless(has_simulator(), "Requires simulator")
class TestExternalRunScripts(unittest.TestCase):
    """
    Test that installation works
    """

    def setUp(self):
        print("\n::group::Log")
        sys.stdout.flush()

    def tearDown(self):
        print("\n::endgroup::")
        sys.stdout.flush()

    def test_exercise_01(self):
        self.check("exercise_01")

    def test_exercise_02(self):
        self.check("exercise_02")

    def test_exercise_03(self):
        self.check("exercise_03")

    def test_exercise_04(self):
        self.check("exercise_04", exit_code=1)
        check_report(
            self.report_file,
            [
                ("passed", "tb_lib.tb_log_and_check.Test 2 - Multiline messages"),
                ("passed", "tb_lib.tb_log_and_check.Test 3 - Printing"),
                ("passed", "tb_lib.tb_log_and_check.Test 5 - Show and hide"),
                ("passed", "tb_lib.tb_log_and_check.Test 6 - Custom log levels"),
                ("passed", "tb_lib.tb_log_and_check.Test 8 - Custom loggers"),
                (
                    "passed",
                    "tb_lib.tb_log_and_check.Test 9 - Giving a logger to a verification component and then control its logging behavior",
                ),
                ("passed", "tb_lib.tb_log_and_check.Test 10 - Adding a file handler"),
                ("passed", "tb_lib.tb_log_and_check.Test 11 - Location preprocessing"),
                (
                    "failed",
                    "tb_lib.tb_log_and_check.Test 1 - Basic logging on the display",
                ),
                ("failed", "tb_lib.tb_log_and_check.Test 4 - Stop level"),
                ("failed", "tb_lib.tb_log_and_check.Test 7 - Checking"),
            ],
        )

    def test_exercise_05(self):
        self.check("exercise_05")

    def test_exercise_06(self):
        self.check("exercise_06")

    def test_exercise_07(self):
        self.check("exercise_07")

    def check(self, exercise, args=None, vhdl_standard="2008", exit_code=0):
        """
        Run external run file and verify exit code
        """
        new_env = environ.copy()
        new_env["VUNIT_VHDL_STANDARD"] = vhdl_standard
        run_file = ROOT / exercise / "solution/run.py"
        self.output_path = run_file.parent / "vunit_out"
        self.report_file = self.output_path / "xunit.xml"
        self.assertEqual(
            call(
                [
                    executable,
                    run_file,
                    "--clean",
                    "--output-path=%s" % self.output_path,
                    "--xunit-xml=%s" % self.report_file,
                ]
                + (args if args is not None else []),
                env=new_env,
            ),
            exit_code,
        )

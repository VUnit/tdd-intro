import unittest
from os import environ
from pathlib import Path
from subprocess import call
import sys
from tests.common import check_report
from vunit.sim_if.common import has_simulator, simulator_is, simulator_check

ROOT = Path(__file__).resolve().parent


@unittest.skipUnless(has_simulator(), "Requires simulator")
class TestExternalRunScripts(unittest.TestCase):
    """
    Test that installation works
    """

    def test_exercise_01(self):
        self.check(ROOT/ "exercise_01"/ "solution"/ "run.py")

    def test_exercise_02(self):
        self.check(ROOT/ "exercise_02"/ "solution"/ "run.py")

    def test_exercise_03(self):
        self.check(ROOT/ "exercise_03"/ "solution"/ "run.py")

    def test_exercise_04(self):
        self.check((ROOT/ "exercise_04"/ "solution"/ "run.py"), exit_code=1)
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
        self.check(ROOT/ "exercise_05"/ "solution"/ "run.py")

    def test_exercise_06(self):
        self.check(ROOT/ "exercise_06"/ "solution"/ "run.py")

    def test_exercise_07(self):
        self.check(ROOT/ "exercise_07"/ "solution"/ "run.py")

    def check(self, run_file, args=None, vhdl_standard="2008", exit_code=0):
        """
        Run external run file and verify exit code
        """
        print(run_file)
        args = args if args is not None else []
        new_env = environ.copy()
        new_env["VUNIT_VHDL_STANDARD"] = vhdl_standard
        self.output_path = (run_file.parent/ "vunit_out")
        self.report_file = (self.output_path/ "xunit.xml")
        retcode = call(
            [
                sys.executable,
                run_file,
                "--clean",
                "--output-path=%s" % self.output_path,
                "--xunit-xml=%s" % self.report_file,
            ]
            + args,
            env=new_env,
        )
        self.assertEqual(retcode, exit_code)
        
if __name__ == "__main__":
    unittest.main()
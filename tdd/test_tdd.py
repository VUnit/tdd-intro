import sys
from sys import executable, platform
from pathlib import Path
from subprocess import check_call, STDOUT
from shutil import which
import unittest


class TestExamples(unittest.TestCase):
    """
    Verify that example run scripts work correctly
    """

    def setUp(self):
        self.shell = [which("bash")] if platform == "win32" else []
        self.root = Path(__file__).parent

        print("\n::group::Log")
        sys.stdout.flush()

    def tearDown(self):
        print("\n::endgroup::")
        sys.stdout.flush()

    def _sh(self, args):
        check_call(self.shell + args, stderr=STDOUT)

    def _py(self, args):
        check_call([executable] + args, stderr=STDOUT)

    def test_vunit_runpy(self):
        self._py([str(self.root / "run.py"), "-v"])

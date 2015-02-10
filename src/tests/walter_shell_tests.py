"""
Unit tests for WalterShell class.

"""
# Author: Andy Holt
# Date: Tue 10 Feb 2015 22:40

import subprocess
import unittest
import walter_shell

class WalterShellTests(unittest.TestCase):
    """
    Unit test suite for WalterShell class.
    """
    @classmethod
    def setUpClass(self):
        """
        Initialisation before running test class (run only once).
        """
        # [todo] - need some method of providing a consistent database
        # experience. Perhaps mocking is the way to go.


    def setUp(self):
        """
        Initialisation for tests.
        """
        self.ws = walter_shell.WalterShell()
        # [review] - probably need to run self.ws.preloop() here

    def tearDown(self):
        """
        Tidy up after running test.
        """
        # [review] - probably run self.ws.postloop() here
        self.ws.onecmd('exit')

    def test_list_default(self):
        """
        Ensure transactions are listed for `list` command.
        """

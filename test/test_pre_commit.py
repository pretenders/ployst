import unittest

from pre_commit import bash


class TestBash(unittest.TestCase):

    def test_run_single_command(self):
        response = bash('ls -la').output
        self.assertTrue("fabfile.py" in response)
        self.assertTrue("bower.json" in response)

    def test_run_piped_command(self):
        response = bash('ls -la | grep fabfile.py').output
        self.assertTrue("fabfile.py" in response)
        self.assertFalse("bower.json" in response)

    def test_concat_command_run(self):
        response = bash('ls -la').bash('grep fabfile.py').output
        self.assertTrue("fabfile.py" in response)
        self.assertFalse("bower.json" in response)

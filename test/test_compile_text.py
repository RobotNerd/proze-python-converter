from dotmap import DotMap
import lib.config
import os
import proze
import unittest

PATH = 'test/sample/tmp/output.txt'


class TestCompileText(unittest.TestCase):

    """Tests for compiling proze projects using the text strategy."""

    def setUp(self):
        try:
            os.remove(PATH)
        except OSError:
            pass

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = PATH[:-4]
        args.path = 'test/sample/no_data'
        proze.run(args)
        self.assertFalse(os.path.isfile(PATH))

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = PATH[:-4]
        args.path = 'test/sample/missing_data'
        proze.run(args)
        with open(PATH) as f:
            self.assertEqual(f.read(), '')

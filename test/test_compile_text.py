from dotmap import DotMap
import os
import proze
import test.expected_text as expected
import unittest

PATH = 'test/sample/tmp/output.txt'
projects = DotMap()
projects.dark_and_stormy = 'test/sample/dark-and-story'
projects.feelings = 'test/sample/feelings'
projects.missing = 'test/sample/missing_data'
projects.no_data = 'test/sample/no_data'


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
        args.path = projects.no_data
        proze.run(args)
        self.assertFalse(os.path.isfile(PATH))

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = PATH[:-4]
        args.path = projects.missing
        proze.run(args)
        with open(PATH) as f:
            self.assertEqual(f.read(), '')

#    def test_compile_with_config(self):
#        """Compile a prose project to text using the config file."""
#        args = DotMap()
#        args.doctype = 'txt'
#        args.output = PATH[:-4]
#        args.path = projects.dark_and_stormy
#        proze.run(args)
#        with open(PATH) as f:
#            self.assertEqual(f.read(), expected.dark_and_stormy())

from dotmap import DotMap
import os
import proze
import test.expected_text as expected
import unittest

OUTPUT_PATH = 'test/sample/tmp/output.txt'
projects = DotMap()
projects.dark_and_stormy = 'test/sample/dark-and-story'
projects.feelings = 'test/sample/feelings'
projects.missing = 'test/sample/missing_data'
projects.no_data = 'test/sample/no_data'
projects.pumpkins.project = 'test/sample/pumpkins'
projects.pumpkins.expected = 'test/sample/pumpkins/pumpkins.txt'


class TestCompileText(unittest.TestCase):

    """Tests for compiling proze projects using the text strategy."""

    def setUp(self):
        try:
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = OUTPUT_PATH[:-4]
        args.path = projects.no_data
        proze.run(args)
        self.assertFalse(os.path.isfile(OUTPUT_PATH))

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = OUTPUT_PATH[:-4]
        args.path = projects.missing
        proze.run(args)
        with open(OUTPUT_PATH) as f:
            self.assertEqual(f.read(), '')

#    def test_compile_with_config(self):
#        """Compile a prose project to text using the config file."""
#        args = DotMap()
#        args.doctype = 'txt'
#        args.output = OUTPUT_PATH[:-4]
#        args.path = projects.dark_and_stormy
#        proze.run(args)
#        with open(OUTPUT_PATH) as f:
#            self.assertEqual(f.read(), expected.dark_and_stormy())

    # def test_pumpkins(self):
    #     """Compile the pumpkins sample project."""
    #     args = DotMap()
    #     args.doctype = 'txt'
    #     args.output = OUTPUT_PATH[:-4]
    #     args.path = projects.pumpkins.project
    #     proze.run(args)
    #     with open(OUTPUT_PATH, 'r') as output:
    #         with open(projects.pumpkins.expected, 'r') as expected:
    #             line1, line2 = output.readline(), expected.readline()
    #             while (
    #                 line1 == line2 and
    #                 line1 is not None and
    #                 line2 is not None
    #             ):
    #                 line1, line2 = output.readline(), expected.readline()
    #             self.assertEqual(line1, line2)

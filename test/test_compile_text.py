from collections import namedtuple
from test.mock import MockArgs
import os
import proze
import test.expected_text as expected
import unittest

OUTPUT_PATH = 'test/sample/tmp/output.txt'

Case = namedtuple('Case', ['root_path', 'expected_output'])
dark_and_stormy = Case('test/sample/dark-and-story', '')
feelings = Case('test/sample/feelings', '')
missing = Case('test/sample/missing_data', '')
no_data = Case('test/sample/no_data', '')
pumpkins = Case(
    'test/sample/pumpkins',
    'test/sample/pumpkins/pumpkins.txt'
)


class TestCompileText(unittest.TestCase):

    """Tests for compiling proze projects using the text strategy."""

    def setUp(self):
        try:
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = MockArgs('txt', OUTPUT_PATH[:-4], no_data.root_path)
        proze.run(args)
        self.assertFalse(os.path.isfile(OUTPUT_PATH))

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = MockArgs('txt', OUTPUT_PATH[:-4], missing.root_path)
        proze.run(args)
        with open(OUTPUT_PATH) as f:
            self.assertEqual(f.read(), '')

    # def test_compile_with_config(self):
    #     """Compile a prose project to text using the config file."""
    #     args = DotMap()
    #     args.doctype = 'txt'
    #     args.output = OUTPUT_PATH[:-4]
    #     args.path = projects.dark_and_stormy
    #     proze.run(args)
    #     with open(OUTPUT_PATH) as f:
    #         self.assertEqual(f.read(), expected.dark_and_stormy())

    def test_pumpkins(self):
        """Compile the pumpkins sample project."""
        args = MockArgs('txt', OUTPUT_PATH[:-4], pumpkins.root_path)
        proze.run(args)
        with open(OUTPUT_PATH, 'r') as generated:
            text_generated = generated.read()
        with open(pumpkins.expected_output, 'r') as expected:
            text_expected = expected.read()
        generated_lines = text_generated.split('\n')
        expected_lines = text_expected.split('\n')
        self.assertEqual(len(generated_lines), len(expected_lines))
        for i in range(0, len(expected_lines)):
            self.assertEqual(generated_lines[i], expected_lines[i])

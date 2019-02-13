from collections import namedtuple
from test.mock import MockArgs
import os
import proze
import unittest

# The output of all test projects are compiled to the same file.
OUTPUT_PATH = 'test/sample/tmp/output.txt'

Case = namedtuple('Case', ['root_path', 'expected_output'])
dark_and_stormy = Case(
    'test/sample/dark-and-story',
    'test/sample/dark-and-story/dark-and-stormy.txt'
)
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

    def load_files(self, generated_path, expected_path):
        """Load data for comparison.
        :param str generated_path: Path to generated output file.
        :param str expected_path: Path to expected data file.
        :return tuple(list, list): Lines of generated text, lines of
            expected text.
        """
        with open(generated_path, 'r') as generated:
            text_generated = generated.read()
        with open(expected_path, 'r') as expected:
            text_expected = expected.read()
        generated_lines = text_generated.split('\n')
        expected_lines = text_expected.split('\n')
        return generated_lines, expected_lines

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = MockArgs(
            doctype='txt',
            output=OUTPUT_PATH[:-4],
            path=no_data.root_path)
        proze.run(args)
        self.assertFalse(os.path.isfile(OUTPUT_PATH))

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = MockArgs(
            doctype='txt',
            output=OUTPUT_PATH[:-4],
            path=missing.root_path)
        proze.run(args)
        with open(OUTPUT_PATH) as f:
            self.assertEqual(f.read(), '')

    def test_dark_and_stormy(self):
        """Compile the dark-and-stormy sample project."""
        args = MockArgs(
            doctype='txt',
            output=OUTPUT_PATH[:-4],
            path=dark_and_stormy.root_path
        )
        proze.run(args)
        generated_lines, expected_lines = self.load_files(
            OUTPUT_PATH,
            dark_and_stormy.expected_output
        )
        self.assertEqual(len(generated_lines), len(expected_lines))
        for i in range(0, len(expected_lines)):
            self.assertEqual(generated_lines[i], expected_lines[i])

    def test_pumpkins(self):
        """Compile the pumpkins sample project."""
        args = MockArgs(
            doctype='txt',
            output=OUTPUT_PATH[:-4],
            path=pumpkins.root_path
        )
        proze.run(args)
        generated_lines, expected_lines = self.load_files(
            OUTPUT_PATH,
            pumpkins.expected_output
        )
        self.assertEqual(len(generated_lines), len(expected_lines))
        for i in range(0, len(expected_lines)):
            self.assertEqual(generated_lines[i], expected_lines[i])

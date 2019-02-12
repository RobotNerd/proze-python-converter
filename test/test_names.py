from test.mock import MockOptions
from lib.names import Names
import unittest


class TestNames(unittest.TestCase):

    def test_find_invalid(self):
        """Check a line of text for invalid names."""
        options = MockOptions()
        options.names.invalid = ['Aaron', 'Gilbert', 'fillerator', ]
        names = Names(options)
        lines = [
            [
                'This has no invalid names.',
                [],
            ],
            [
                'His name was Aaron but he went buy Jerry.',
                ['Aaron'],
            ],
            [
                '"Hush Aaron," gilbert said.',
                ['Aaron', 'Gilbert'],
            ],
            [
                'The fillerator is the best appliance in the store!',
                ['fillerator'],
            ],
        ]
        for line in lines:
            self.assertEqual(names.find_invalid(line[0]), line[1])

    def test_invalid_with_punctuation(self):
        """Check for invalid names adjacent to punctuation marks."""
        options = MockOptions()
        options.names.invalid = ['Aaron', 'Gilbert', 'FILLERATOR']
        names = Names(options)
        lines = [
            [
                'Aaron\'s bike was expensive.',
                ['Aaron'],
            ],
            [
                'Gilbert,Aaron',
                ['Aaron', 'Gilbert'],
            ],
            [
                'Fillerator! This looks dirty.',
                ['FILLERATOR'],
            ],
        ]
        for line in lines:
            self.assertEqual(names.find_invalid(line[0]), line[1])

    def test_invalid_inside_other_word(self):
        """It should not flag invalid words embedded inside a larger word."""
        options = MockOptions()
        options.names.invalid = ['ing', 'owe']
        names = Names(options)
        lines = [
            [
                'lowerings',
                [],
            ],
            [
                'He owes you nothing',
                [],
            ],
        ]
        for line in lines:
            self.assertEqual(names.find_invalid(line[0]), line[1])

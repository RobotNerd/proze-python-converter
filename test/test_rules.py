from dotmap import DotMap
from lib.rules import Rules
import unittest


class TestNames(unittest.TestCase):

    def test_find_invalid(self):
        """Clean up whitespace."""
        options = DotMap()
        rules = Rules(options)
        lines = [
            [
                ' Whitespace is removed from either end of the line. ',
                'Whitespace is removed from either end of the line.',
            ],
            [
                '   Whitespace is removed from either end of the line.   ',
                'Whitespace is removed from either end of the line.',
            ],
            [
                'Multiple spaces          are merged into a space.',
                'Multiple spaces are merged into a space.',
            ],
            [
                '\tTabs are merged\t\tinto single spaces.\t\t',
                'Tabs are merged into single spaces.',
            ],
            [
                '\tMixed whitespace is      \t treated the same.\t\t',
                'Mixed whitespace is treated the same.',
            ],
        ]
        for line in lines:
            self.assertEqual(rules.clean_whitespace(line[0]), line[1])

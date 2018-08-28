from dotmap import DotMap
from lib.names import Names
import unittest


class TestNames(unittest.TestCase):

    def test_find_invalid(self):
        """Test checking a line of text for invalid names."""
        options = DotMap()
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

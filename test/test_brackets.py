from dotmap import DotMap
from lib.brackets import Brackets
import unittest


class TestBrackets(unittest.TestCase):

    def test_on_same_line(self):
        """Brackets open and close on same line."""
        lines = [
            [
                'abcd [hidden] efg',
                'abcd  efg',
            ],
            [
                'abcd[hidden]efg',
                'abcdefg',
            ],
            [
                '[ hidden ]',
                '',
            ],
            [
                '  [ hidden ]  ',
                '    ',
            ],
        ]
        brackets = Brackets()
        for line in lines:
            brackets.reset()
            self.assertEqual(brackets.remove(line[0]), line[1])

    def test_comment_tokens_in_block(self):
        """Comment tokens aren't recognized inside bracket blocks."""
        lines = [
            [
                'abcd [ hidden ### hidden ] ef',
                'abcd  ef',
            ],
            [
                'abcd [ ## hidden ## hidden ] efg',
                'abcd  efg',
            ],
        ]
        brackets = Brackets()
        for line in lines:
            brackets.reset()
            self.assertEqual(brackets.remove(line[0]), line[1])

    def test_block_wrapping(self):
        """A bracket block that wraps over multiple lines."""
        cases = [
            [
                [
                    'abcd [ inside block',
                    'abcd ',
                ],
                [
                    'inside block ] efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd',
                    'abcd',
                ],
                [
                    'abcd [ inside block',
                    'abcd ',
                ],
                [
                    'inside block',
                    '',
                ],
                [
                    'inside block comment ] efg',
                    ' efg',
                ]
            ],
        ]
        brackets = Brackets()
        for lines in cases:
            brackets.reset()
            for line in lines:
                self.assertEqual(brackets.remove(line[0]), line[1])

    def test_multiple_blocks(self):
        """Lines that have multiple blocks."""
        lines = [
            [
                'a [ test ] b [ test ] c',
                'a  b  c',
            ],
            [
                'a [ test ] bcde [ f g ]',
                'a  bcde ',
            ],
            [
                'a [ test ] bcde [ f g',
                'a  bcde ',
            ],
        ]
        brackets = Brackets()
        for line in lines:
            brackets.reset()
            self.assertEqual(brackets.remove(line[0]), line[1])

    def test_no_brackets(self):
        """A line that doesn't have any brackets."""
        lines = [
            '"Furthermore," she said, "I would never take a deal like that."',
            'Use the hashtag #withoutHoldings on that post.',
            'Nothing looks right in here.',
            '',
        ]
        brackets = Brackets()
        for line in lines:
            self.assertEqual(brackets.remove(line), line)

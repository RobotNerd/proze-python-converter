from dotmap import DotMap
from lib.comments import Comments
import unittest


class TestComments(unittest.TestCase):

    def test_block(self):
        """Normal usage of a block comment."""
        lines = [
            [
                'abcd ### hidden ### efg',
                'abcd  efg',
            ],
            [
                '### hidden ###',
                '',
            ],
            [
                '  ### hidden ###  ',
                '    ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_block_no_spacing(self):
        """Block tokens without spacing between them."""
        lines = [
            [
                'abcd ### hidden ###### also hidden ### ef',
                'abcd  ef',
            ],
            [
                'abcd### hidden ###ef',
                'abcdef',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_block_hides_line(self):
        """A line comment token is hidden by a block token."""
        lines = [
            [
                'abcd ### test of hidden ## token ### ef',
                'abcd  ef',
            ],
            [
                'abcd ### test of hidden ## token',
                'abcd ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_block_line_adjacent(self):
        """A line comment is adjacent to the ending block comment."""
        lines = [
            [
                'abcd ### test of hidden ##### and this is hidden too',
                'abcd ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_block_wrapping(self):
        """Test a block comment wrapping across multiple lines."""
        cases = [
            [
                [
                    'abcd ### inside block comment',
                    'abcd ',
                ],
                [
                    'inside block comment ### efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd',
                    'abcd',
                ],
                [
                    'abcd ### inside block comment',
                    'abcd ',
                ],
                [
                    'inside block comment',
                    '',
                ],
                [
                    'inside block comment ### efg',
                    ' efg',
                ]
            ],
        ]
        comments = Comments()
        for lines in cases:
            comments.reset()
            for line in lines:
                self.assertEqual(comments.remove(line[0]), line[1])

    def test_line_hides_block(self):
        """A block comment token is hidden by a line token."""
        lines = [
            [
                'abcd ## test of ### hidden block ### comment token',
                'abcd ',
            ],
            [
                'abcd ## test of ### hidden block comment token',
                'abcd ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_line_token(self):
        """Normal usage of a line comment token."""
        lines = [
            [
                'abcd ## The rest of the line is hidden',
                'abcd ',
            ],
            [
                'abcd ##',
                'abcd ',
            ],
            [
                '## The entire line is hidden',
                '',
            ],
            [
                ' ## The entire line is hidden',
                ' ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_multiple_blocks(self):
        """Lines that have multiple block comments."""
        lines = [
            [
                'a ### test ### b ### test ### c',
                'a  b  c',
            ],
            [
                'a ### test ### bcde ### f g ###',
                'a  bcde ',
            ],
            [
                'a ### test ### bcde ### f g',
                'a  bcde ',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])

    def test_no_comment(self):
        """A line that doesn't have any comments."""
        lines = [
            '"Furthermore," she said, "I would never take a deal like that."',
            'Use the hashtag #withoutHoldings on that post.',
            'Nothing looks right in here.',
            '',
        ]
        comments = Comments()
        for line in lines:
            self.assertEqual(comments.remove(line), line)

from dotmap import DotMap
from lib.blocks import Blocks
import unittest


class TestBlocks(unittest.TestCase):

    def test_brackets_hide_comments(self):
        """A bracket block hiding comment tokens."""
        lines = [
            [
                'abcd [ test of ### hidden block ### comment token ]',
                'abcd ',
            ],
            [
                'abcd [ test of ## hidden block comment token]',
                'abcd ',
            ],
            [
                'abcd [ test of ### hidden block ### comment token ] efg',
                'abcd  efg',
            ],
            [
                'abcd [ test of ## hidden block comment token ] efg',
                'abcd  efg',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_brackets_on_same_line(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_brackets_wrapping(self):
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
        blocks = Blocks()
        for lines in cases:
            blocks.reset()
            for line in lines:
                self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_block(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_block_no_spacing(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_block_hides_line_comment(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_block_line_comment_adjacent(self):
        """A line comment is adjacent to the ending block comment."""
        lines = [
            [
                'abcd ### test of hidden ##### and this is hidden too',
                'abcd ',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_block_wrapping(self):
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
            [
                [
                    'abcd ### inside block comment',
                    'abcd ',
                ],
                [
                    'this is all ## inside block comment',
                    '',
                ],
                [
                    'inside block comment ### efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd ## this will not start ### a block comment',
                    'abcd ',
                ],
                [
                    'abcd ### inside block comment',
                    'abcd ',
                ],
                [
                    'this is all ## inside block comment',
                    '',
                ],
                [
                    'inside block comment ### efg',
                    ' efg',
                ]
            ],
        ]
        blocks = Blocks()
        for lines in cases:
            blocks.reset()
            for line in lines:
                self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comments_hide_brackets(self):
        """A comment token hides a bracket block."""
        lines = [
            [
                'abcd ## test of [ hidden block ] comment token',
                'abcd ',
            ],
            [
                'abcd ### test of [ hidden block ] comment token',
                'abcd ',
            ],
            [
                'abcd ### test of [ hidden block ] comment token ### efg',
                'abcd  efg',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_escape_brackets(self):
        """Bracket tokens aren't matched if they are escaped."""
        lines = [
            [
                r'abcd \[ efg',
                r'abcd \[ efg',
            ],
            [
                r'abcd \[ efg [ this is hidden ]',
                r'abcd \[ efg ',
            ],
            [
                r'abcd \[ efg [ this is hidden \] hij ]',
                r'abcd \[ efg ',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_escape_comment_block(self):
        """Bracket tokens aren't matched if they are escaped."""
        lines = [
            [
                r'abcd \### efg',
                r'abcd \### efg',
            ],
            [
                r'abcd \### efg ## test',
                r'abcd \### efg ',
            ],
            [
                r'abcd \### efg ### test \### test ### hij',
                r'abcd \### efg  hij',
            ],
            [
                r'abcd \### efg ### test \### test \## ### hij',
                r'abcd \### efg  hij',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_escape_comment_line(self):
        """Bracket tokens aren't matched if they are escaped."""
        lines = [
            [
                r'abcd \## efg',
                r'abcd \## efg',
            ],
            [
                r'abcd \## efg ## test',
                r'abcd \## efg ',
            ],
            [
                r'abcd ## efg ## test',
                r'abcd ',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_line_comment_hides_block_comment(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_line_comment_token(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_multiple_brackets_per_line(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_multiple_comment_blocks(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_multiple_mixed_comment_bracket_blocks(self):
        """Lines that have multiple block comments."""
        lines = [
            [
                'a ### test ### b [ test ] c',
                'a  b  c',
            ],
            [
                'a [ test] bcde ### f g ###',
                'a  bcde ',
            ],
            [
                'a ### test ### bcde [ f g',
                'a  bcde ',
            ],
        ]
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_comment_tokens_in_brackets(self):
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
        blocks = Blocks()
        for line in lines:
            blocks.reset()
            self.assertEqual(blocks.remove(line[0]), line[1])

    def test_no_blocks(self):
        """A line that doesn't have any comments."""
        lines = [
            '"Furthermore," she said, "I would never take a deal like that."',
            'Use the hashtag #withoutHoldings on that post.',
            'Nothing looks right in here.',
            '',
        ]
        blocks = Blocks()
        for line in lines:
            self.assertEqual(blocks.remove(line), line)

    def test_wrapped_blocks_hiding(self):
        """Test wrapped blocks hiding each other.."""
        cases = [
            [
                [
                    'abcd ### inside block comment',
                    'abcd ',
                ],
                [
                    '[inside block comment ### efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd [ inside block comment',
                    'abcd ',
                ],
                [
                    '###inside block comment ] efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd',
                    'abcd',
                ],
                [
                    'abcd ### inside block ] comment',
                    'abcd ',
                ],
                [
                    'inside block [ comment',
                    '',
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
                    'abcd [ inside block ### comment',
                    'abcd ',
                ],
                [
                    'inside block comment',
                    '',
                ],
                [
                    'inside block comment ] efg',
                    ' efg',
                ]
            ],
            [
                [
                    'abcd ## hidden by [ line comment',
                    'abcd ',
                ],
                [
                    'efg',
                    'efg',
                ]
            ],
        ]
        blocks = Blocks()
        for lines in cases:
            blocks.reset()
            for line in lines:
                self.assertEqual(blocks.remove(line[0]), line[1])

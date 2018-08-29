from dotmap import DotMap
from lib.comments import Comments
import unittest


class TestComments(unittest.TestCase):

    def test_no_comment(self):
        """Test a proze line that doesn't have any comments."""
        lines = [
            '"Furthermore," she said, "I would never take a deal like that."',
            'Use the hashtag #withoutHoldings on that post.',
            'Nothing looks right in here.',
            '',
        ]
        comments = Comments()
        for line in lines:
            self.assertEqual(comments.remove(line), line)

    def test_multiple_blocks(self):
        lines = [
            [
                'a ### test ### b ### test ### c',
                'a  b  c',
            ],
            [
                'a ### test ### bcde ### f g ###',
                'a  bcde',
            ],
            [
                'a ### test ### bcde ### f g',
                'a  bcde',
            ],
        ]
        comments = Comments()
        for line in lines:
            comments.reset()
            self.assertEqual(comments.remove(line[0]), line[1])


# TODO test cases
#   - line comment hiding block comment
#   - block comment hiding line comment
#   - block comment from previous line
#       - current line entirely commented out by blokc
#       - block comment ends on current line
#   - block comment continuing onto next line
#   - line comment first thing on the line
#   - line comment last thing on the line
#   - block comment takes up entire line
#   - more than 3 adjacent # characters (e.g. ######)

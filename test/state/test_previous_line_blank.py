from dotmap import DotMap
import lib.state
import unittest


class TestStatePreviousLineBlank(unittest.TestCase):

    """Check if previous line is considered to be a blank line."""

    def test_previous_line_blank(self):
        """Track state when previous line is blank."""
        state = lib.state.State()
        self.assertTrue(state.is_previous_line_blank)
        state.update('')
        self.assertTrue(state.is_previous_line_blank)
        state.update('     ')
        self.assertTrue(state.is_previous_line_blank)
        state.update('\t')
        self.assertTrue(state.is_previous_line_blank)
        state.update('\t    \t   ')
        self.assertTrue(state.is_previous_line_blank)
        state.update('a')
        self.assertFalse(state.is_previous_line_blank)
        state.update('Chapter: test')
        self.assertTrue(state.is_previous_line_blank)
        self.assertFalse(state.is_markup_line)

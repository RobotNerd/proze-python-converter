from dotmap import DotMap
import lib.state
import unittest


class TestStatePreviousLineBlank(unittest.TestCase):

    """Check if previous line is considered to be a blank line."""

    def test_empty_string(self):
        state = lib.state.State()
        self.assertTrue(state.is_previous_line_blank)
        state.update('')
        self.assertTrue(state.is_previous_line_blank)

    def test_spaces(self):
        state = lib.state.State()
        state.update('     ')
        self.assertTrue(state.is_previous_line_blank)

    def test_mix_tabs_spaces(self):
        state = lib.state.State()
        state.update('\t')
        self.assertTrue(state.is_previous_line_blank)
        state.update('\t    \t   ')
        self.assertTrue(state.is_previous_line_blank)

    def test_not_a_blank_line(self):
        state = lib.state.State()
        state.update('a')
        self.assertFalse(state.is_previous_line_blank)

    def test_structural_markup(self):
        state = lib.state.State()
        state.update('Chapter: test')
        self.assertTrue(state.is_previous_line_blank)
        self.assertTrue(state.markup.is_markup_line)

    def test_structural_markup_previous_not_blank(self):
        state = lib.state.State()
        state.update('a')
        state.update('Chapter: test')
        self.assertFalse(state.is_previous_line_blank)
        self.assertFalse(state.markup.is_markup_line)

from dotmap import DotMap
import lib.state
import unittest

proze_line = 'a line of proze text'


class TestStatePreviousLineBlank(unittest.TestCase):

    """Check if previous line is considered to be a blank line."""

    def test_empty_string(self):
        state = lib.state.State()
        self.assertTrue(state.previous_line.is_blank)
        state.update('')
        state.update(proze_line)
        self.assertTrue(state.previous_line.is_blank)

    def test_spaces(self):
        state = lib.state.State()
        state.update('     ')
        state.update(proze_line)
        self.assertTrue(state.previous_line.is_blank)

    def test_mix_tabs_spaces(self):
        state = lib.state.State()
        state.update('\t')
        state.update(proze_line)
        self.assertTrue(state.previous_line.is_blank)
        state.update('\t    \t   ')
        state.update(proze_line)
        self.assertTrue(state.previous_line.is_blank)

    def test_not_a_blank_line(self):
        state = lib.state.State()
        state.update('a')
        self.assertTrue(state.previous_line.is_blank)

    def test_structural_markup(self):
        state = lib.state.State()
        state.update('')
        state.update('Chapter: test')
        self.assertTrue(state.markup.is_markup_line)
        self.assertTrue(state.previous_line.is_blank)

    def test_structural_markup_previous_not_blank(self):
        state = lib.state.State()
        state.update('a')
        state.update('Chapter: test')
        self.assertFalse(state.previous_line.is_blank)
        self.assertFalse(state.markup.is_markup_line)

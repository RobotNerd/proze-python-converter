from dotmap import DotMap
import lib.state
import unittest


class TestStateItalicsWrapping(unittest.TestCase):

    """Tests for tracking state of iatlics blocks over multiple lines."""

    def test_hanging_closed_by_bold_token(self):
        """Wraps multiple lines and closed by token."""
        state = lib.state.State()
        self.assertFalse(state.is_italics)
        state.update('*test')
        state.update('more proze')
        self.assertTrue(state.is_italics)
        state.update('*')
        self.assertFalse(state.is_italics)

    def test_hanging_closed_by_newline(self):
        """Wraps multiple lines and is closed by an empty line."""
        state = lib.state.State()
        self.assertFalse(state.is_italics)
        state.update('*test')
        state.update('more proze')
        self.assertTrue(state.is_italics)
        state.update('   ')
        self.assertFalse(state.is_italics)

    def test_multiple_hanging_open(self):
        """Multiple bold blocks on a line with the last one staying open."""
        state = lib.state.State()
        self.assertFalse(state.is_italics)
        state.update('*test* and * test')
        self.assertTrue(state.is_italics)

    def test_one_line(self):
        """A single line with a single bold block that closes itself."""
        state = lib.state.State()
        self.assertFalse(state.is_italics)
        state.update('*test*')
        self.assertFalse(state.is_italics)

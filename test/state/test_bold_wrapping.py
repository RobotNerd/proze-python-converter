import lib.state
import unittest


class TestStateBoldWrapping(unittest.TestCase):

    """Tests for tracking state of bold blocks over multiple lines."""

    def test_hanging_closed_by_bold_token(self):
        """Wraps multiple lines and closed by token."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('__')
        self.assertFalse(state.is_bold)

    def test_hanging_closed_by_newline(self):
        """Wraps multiple lines and is closed by an empty line."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('   ')
        self.assertFalse(state.is_bold)

    def test_multiple_hanging_open(self):
        """Multiple bold blocks on a line with the last one staying open."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test__ and __ test')
        self.assertTrue(state.is_bold)

    def test_one_line(self):
        """A single line with a single bold block that closes itself."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test__')
        self.assertFalse(state.is_bold)

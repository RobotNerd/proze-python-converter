from dotmap import DotMap
import lib.state
import unittest

proze_line = 'a line of proze text'


class TestStateItalicsWrapping(unittest.TestCase):

    """Tests for tracking state of iatlics blocks over multiple lines."""

    def test_italics_wrapping(self):
        """Bold formatting wraps from the previous line."""
        state = lib.state.State()
        self.assertFalse(state.is_italics)
        state.update('*test*')
        self.assertFalse(state.is_italics)
        state.update('*test* and * test')
        self.assertTrue(state.is_italics)
        state.reset()
        self.assertFalse(state.is_italics)
        state.update('*test')
        state.update('more proze')
        self.assertTrue(state.is_italics)
        state.update('*')
        self.assertFalse(state.is_italics)
        state.reset()
        state.update('*test')
        state.update('more proze')
        self.assertTrue(state.is_italics)
        state.update('   ')
        self.assertFalse(state.is_italics)

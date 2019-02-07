from dotmap import DotMap
import lib.blocks
import lib.state
import unittest


class TestIndented(unittest.TestCase):

    """Tests for block quotes."""

    # TODO split this test case into smaller, more focused tests
    def test_indented_blockquote(self):
        """A paragraph indented as a block quotes."""
        state = lib.state.State()
        self.assertEqual(state.indent_level, 0)
        state.update('    a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update(' ')
        self.assertEqual(state.indent_level, 1)
        state.update('a line of proze')
        self.assertEqual(state.indent_level, 0)
        state.update(' ')
        self.assertEqual(state.indent_level, 0)
        state.update('    a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update('    a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update('     a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update('a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update('')
        self.assertEqual(state.indent_level, 1)
        # This reverts to zero because it's an un-indent that goes negative.
        state.update('\t\ta line of proze')
        self.assertEqual(state.indent_level, 0)
        state.reset()
        state.update('a line of proze')
        self.assertEqual(state.indent_level, 0)

    def test_multiple_levels(self):
        """A paragraph indented as a block quotes."""
        state = lib.state.State()
        self.assertEqual(state.indent_level, 0)
        state.update('    a line of proze')
        self.assertEqual(state.indent_level, 1)
        state.update('    ')
        state.update('        a line of proze')
        self.assertEqual(state.indent_level, 2)
        state.update('    ')
        state.update('    a line of proze')
        self.assertEqual(state.indent_level, 1)

    def test_with_block_comments(self):
        """Interaction with blocks comments."""
        pass

    def test_with_line_comments(self):
        """Interaction with line comments."""
        state = lib.state.State()
        self.assertEqual(state.indent_level, 0)
        state.update('    indented ## with line comment')
        self.assertEqual(state.indent_level, 1)
        state.update('    part of the same indented block')
        self.assertEqual(state.indent_level, 1)
        state.update('## the entire line is commented out')
        self.assertEqual(state.indent_level, 1)
        state.update('part of the same block quote')
        self.assertEqual(state.indent_level, 1)

    def test_with_brackets(self):
        """Interaction with bracketed blocks."""
        pass

    def test_with_structural_tags(self):
        """A chapter/title/sectiont tag in an blockquote."""
        pass

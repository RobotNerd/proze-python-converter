from dotmap import DotMap
import lib.state
import unittest

proze_line = 'a line of proze text'


class TestStateFirstParagraph(unittest.TestCase):

    """Check if the line is considered to be the first paragraph of a block."""

    def test_none_exists(self):
        """No first paragraph found from beginning of file."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        self.assertFalse(state.is_first_paragraph)

    def test_beginning_of_file(self):
        """First paragraph found from beginning of file, no markup."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)

    def test_not_flag_second_paragraph(self):
        """Second paragraph not flagged as being first."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update('')
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)

    def test_second_line_of_paragraph(self):
        """Second lines of paragraphs not flagged as being first line."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)

    def test_after_title(self):
        """Flag first line after title markup as first paragraph."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update(proze_line)
        state.update('')
        state.update('Title: test')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)

    def test_multiple_structural_tags(self):
        """Flag first paragraph after each structure markup tag."""
        state = lib.state.State()
        state.update('Title: test')
        state.update(proze_line)
        state.update('')
        state.update('Chapter: test')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)
        state.update('')
        state.update('Section: test')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)
        state.update('')
        state.update('---')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)

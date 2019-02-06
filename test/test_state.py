from dotmap import DotMap
import lib.state
import unittest

proze_line = 'a line of text'


class TestState(unittest.TestCase):

    """Tests for tracking state of compilation process."""

    def test_bold_wrapping_one_line(self):
        """Bold formatting opened and closed on current line."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test__')
        self.assertFalse(state.is_bold)

    def test_bold_wrapping_multiple_hanging_open(self):
        """Bold formatting, multiple and hanging open."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test__ and __ test')
        self.assertTrue(state.is_bold)

    def test_bold_wrapping_hanging_closed_by_bold_token(self):
        """Bold formatting wraps from the previous line."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('__')
        self.assertFalse(state.is_bold)

    def test_bold_wrapping_hanging_closed_by_newline(self):
        """Bold formatting wraps from the previous line."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('   ')
        self.assertFalse(state.is_bold)

    def test_first_paragraph_none_exists(self):
        """No first paragraph found from beginning of file."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        self.assertFalse(state.is_first_paragraph)

    def test_first_paragraph_beginning_of_file(self):
        """First paragraph found from beginning of file, no markup."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)

    def test_first_paragraph_not_flag_second_paragraph(self):
        """Second paragraph not flagged as being first."""
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update('')
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)

    def test_first_paragraph_second_line_of_paragraph(self):
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

    def test_first_paragraph_after_title(self):
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

    def test_first_paragraph_multiple_structural_tags(self):
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

    def test_in_chapter_or_section(self):
        """Not in a chapter or section."""
        state = lib.state.State()
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('test a line')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('Section: test')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('---')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('Chapter:')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('---stuff')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)
        self.assertFalse(state.is_markup_line)

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

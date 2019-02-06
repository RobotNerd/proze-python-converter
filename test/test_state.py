from dotmap import DotMap
import lib.state
import unittest


class TestState(unittest.TestCase):

    """Tests for tracking state of compilation process."""

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

    def test_first_paragraph(self):
        """Flag first line of the first paragraph.
        Applies after a title, chapter, or section tag.
        """
        proze_line = 'a line of text'
        state = lib.state.State()
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        self.assertFalse(state.is_first_paragraph)
        state.update(proze_line)
        self.assertTrue(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update(proze_line)
        state.update(proze_line)
        self.assertFalse(state.is_first_paragraph)
        state.update('')
        state.update('Title: test')
        state.update(proze_line)
        self.assertFalse(state.is_markup_line)
        self.assertTrue(state.is_first_paragraph)
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

    def test_bold_wrapping(self):
        """Bold formatting wraps from the previous line."""
        state = lib.state.State()
        self.assertFalse(state.is_bold)
        state.update('__test__')
        self.assertFalse(state.is_bold)
        state.update('__test__ and __ test')
        self.assertTrue(state.is_bold)
        state.reset()
        self.assertFalse(state.is_bold)
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('__')
        self.assertFalse(state.is_bold)
        state.reset()
        state.update('__test')
        state.update('more proze')
        self.assertTrue(state.is_bold)
        state.update('   ')
        self.assertFalse(state.is_bold)

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

from dotmap import DotMap
import lib.state
import unittest


class TestStateChapterSection(unittest.TestCase):

    """Track whether the current line is in a chapter or section block."""

    def test_empty_string(self):
        state = lib.state.State()
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_chapter(self):
        state = lib.state.State()
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)
        self.assertTrue(state.is_markup_line)

    def test_section(self):
        state = lib.state.State()
        state.update('Section: test')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertTrue(state.is_markup_line)

    def test_section_break(self):
        state = lib.state.State()
        state.update('---')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertTrue(state.is_markup_line)

    def test_no_previous_blank_line_chapter(self):
        state = lib.state.State()
        state.update('test a line')
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_no_previous_blank_line_section(self):
        state = lib.state.State()
        state.update('test a line')
        state.update('Section: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_no_previous_blank_line_section_break(self):
        state = lib.state.State()
        state.update('test a line')
        state.update('---')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_contiguous_markup_lines(self):
        state = lib.state.State()
        state.update('Title: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertTrue(state.is_markup_line)
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)
        self.assertTrue(state.is_markup_line)
        state.update('Section: test')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertTrue(state.is_markup_line)
        state.update('---')
        self.assertTrue(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertTrue(state.is_markup_line)

    def test_contiguous_markup_lines_no_previous_blank_line(self):
        state = lib.state.State()
        state.update('test a line')
        state.update('Title: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('Section: test')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('---')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_invalid_section_break(self):
        state = lib.state.State()
        state.update('---stuff')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

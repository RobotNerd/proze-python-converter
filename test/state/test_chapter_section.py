from dotmap import DotMap
import lib.state
import unittest


class TestStateChapterSection(unittest.TestCase):

    """Track whether the current line is in a chapter or section block."""

    def test_1(self):
        """Not in a chapter or section."""
        state = lib.state.State()
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)
        state.update('')
        self.assertFalse(state.is_section)
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_2(self):
        """Not in a chapter or section."""
        state = lib.state.State()
        state.update('')
        state.update('test a line')
        state.update('Chapter: test')
        self.assertFalse(state.is_section)
        self.assertTrue(state.is_chapter)  # TODO should be false; no newline
        self.assertFalse(state.is_markup_line)

    def test_3(self):
        """Not in a chapter or section."""
        state = lib.state.State()
        state.update('')
        state.update('test a line')
        state.update('Chapter: test')
        state.update('Section: test')
        self.assertTrue(state.is_section)  # TODO should be false; no newline
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    def test_4(self):
        """Not in a chapter or section."""
        state = lib.state.State()
        state.update('')
        state.update('test a line')
        state.update('Chapter: test')
        state.update('Section: test')
        state.update('---')
        self.assertTrue(state.is_section)  # TODO should be false; no newline
        self.assertFalse(state.is_chapter)
        self.assertFalse(state.is_markup_line)

    # def test_in_chapter_or_section(self):
    #     """Not in a chapter or section."""
    #     state = lib.state.State()
    #     self.assertFalse(state.is_section)
    #     self.assertFalse(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('')
    #     self.assertFalse(state.is_section)
    #     self.assertFalse(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('test a line')
    #     self.assertFalse(state.is_section)
    #     self.assertFalse(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('Chapter: test')
    #     self.assertFalse(state.is_section)
    #     self.assertTrue(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('Section: test')
    #     self.assertTrue(state.is_section)
    #     self.assertFalse(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('---')
    #     self.assertTrue(state.is_section)
    #     self.assertFalse(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('Chapter:')
    #     self.assertFalse(state.is_section)
    #     self.assertTrue(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)
    #     state.update('---stuff')
    #     self.assertFalse(state.is_section)
    #     self.assertTrue(state.is_chapter)
    #     self.assertFalse(state.is_markup_line)

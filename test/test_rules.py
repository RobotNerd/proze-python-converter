from dotmap import DotMap
from lib.rules import Rules
from lib.state import State
import unittest


class TestNames(unittest.TestCase):

    def _create_rules_prose_first_char(self):
        """Create a rules object for inserting characters.
        @rtype:  lib.rules.Rules
        @return: Rules object.
        """
        options = DotMap()
        options.compile.paragraph.mode = 'prose'
        options.compile.paragraph.tabFirst.title = False
        options.compile.paragraph.tabFirst.chapter = True
        options.compile.paragraph.tabFirst.section = True
        return Rules(options)

    def test_clean_whitespace(self):
        """Clean up whitespace."""
        options = DotMap()
        rules = Rules(options)
        lines = [
            [
                ' Whitespace is removed from either end of the line. ',
                'Whitespace is removed from either end of the line.',
            ],
            [
                '   Whitespace is removed from either end of the line.   ',
                'Whitespace is removed from either end of the line.',
            ],
            [
                'Multiple spaces          are merged into a space.',
                'Multiple spaces are merged into a space.',
            ],
            [
                '\tTabs are merged\t\tinto single spaces.\t\t',
                'Tabs are merged into single spaces.',
            ],
            [
                '\tMixed whitespace is      \t treated the same.\t\t',
                'Mixed whitespace is treated the same.',
            ],
        ]
        for line in lines:
            self.assertEqual(rules.clean_whitespace(line[0]), line[1])
    
    def test_first_character_title(self):
        """Don't insert tab in first paragraph in the story."""
        rules = self._create_rules_prose_first_char()
        state = State()
        state.is_previous_line_blank = True
        state.is_first_paragraph = True
        state.is_chapter = False
        state.is_section = False
        self.assertEqual(rules.first_character(state), '')
        rules.options.compile.paragraph.mode = 'justified'
        self.assertEqual(rules.first_character(state), '')

    def test_first_character_not_first_paragraph(self):
        """Insert a tab if it isn't the first paragraph."""
        rules = self._create_rules_prose_first_char()
        state = State()
        state.is_previous_line_blank = True
        state.is_first_paragraph = False
        state.is_chapter = False
        state.is_section = False
        self.assertEqual(rules.first_character(state), '\t')
        rules.options.compile.paragraph.mode = 'justified'
        self.assertEqual(rules.first_character(state), '')

    def test_first_character_not_first_line(self):
        """Don't insert a tab if the previous line isn't blank."""
        rules = self._create_rules_prose_first_char()
        state = State()
        state.is_previous_line_blank = False
        state.is_first_paragraph = False
        state.is_chapter = False
        state.is_section = False
        self.assertEqual(rules.first_character(state), '')
        rules.options.compile.paragraph.mode = 'justified'
        self.assertEqual(rules.first_character(state), '')

    def test_first_character_chapter(self):
        """Insert a tab for first paragraph of a chapter."""
        rules = self._create_rules_prose_first_char()
        state = State()
        state.is_previous_line_blank = True
        state.is_first_paragraph = True
        state.is_chapter = True
        state.is_section = False
        self.assertEqual(rules.first_character(state), '\t')
        rules.options.compile.paragraph.mode = 'justified'
        self.assertEqual(rules.first_character(state), '')

    def test_first_character_section(self):
        """Insert a tab for first paragraph of a section."""
        rules = self._create_rules_prose_first_char()
        state = State()
        state.is_previous_line_blank = True
        state.is_first_paragraph = True
        state.is_chapter = False
        state.is_section = True
        self.assertEqual(rules.first_character(state), '\t')
        rules.options.compile.paragraph.mode = 'justified'
        self.assertEqual(rules.first_character(state), '')

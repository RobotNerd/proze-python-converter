from lib.structural_token import MarkupToken
import re

whitespace = re.compile(r'^(\s+)[^\s-]')

# TODO consider renaming is_previous_line_blank to start_new_paragraph


class MarkupState(object):

    """Track state related to structural markup."""

    def __init__(self):
        # True if inside a chapter.
        self.is_chapter = None

        # True if the current line starts with a structural markup token.
        self.is_markup_line = None

        # True if inside a section.
        self.is_section = None

        # The markup token value. None if current line isn't a markup token.
        self.token = None

        self.reset()

    def reset(self):
        """Reset all state values to default."""
        self.is_chapter = False
        self.is_markup_line = False
        self.is_section = False
        self.token = None

    def is_markup(self, line, is_previous_line_blank):
        """Check if the line is structural markup.
        @type  line: str
        @param line: Lowercase line of proze text.
        @type  is_previous_line_blank: boolean
        @param is_previous_line_blank: True if previous line can be treated
            as a blank line.
        """
        if is_previous_line_blank:
            self.token = None
            if line.startswith(MarkupToken.author):
                self.token = MarkupToken.author
            elif line.startswith(MarkupToken.chapter):
                self.token = MarkupToken.chapter
            elif line.startswith(MarkupToken.section):
                self.token = MarkupToken.section
            elif line.startswith(MarkupToken.title):
                self.token = MarkupToken.title
            elif line.strip() == MarkupToken.section_break:
                self.token = MarkupToken.section_break
            if self.token is not None:
                self.is_markup_line = True

    def update_structural_markup_flags(self, is_previous_line_blank):
        """Update flags based on structural markup token.
        @type  is_previous_line_blank: boolean
        @param is_previous_line_blank: True if previous line can be treated
        """
        is_previous_line_blank = True
        if self.token != MarkupToken.author:
            self._find_first_paragraph = True
        if self.token == MarkupToken.chapter:
            self.is_chapter = True
            self.is_section = False
        elif (
            self.token == MarkupToken.section or
            self.token == MarkupToken.section_break
        ):
            self.is_chapter = False
            self.is_section = True
        else:
            self.is_chapter = False
            self.is_section = False


class State(object):

    """Track current state of document compilation."""

    def __init__(self):
        # When true, the next line of proze is the first paragraph
        # after a new title, chapter, or section.
        self._find_first_paragraph = True

        # Track the indentation level for block quotes.
        self._indent_leading_whitespace = []
        self.indent_level = 0

        # True if bold is carried over from a previous line.
        self.is_bold = None

        # True if currently in the first paragraph after a title,
        # chapter, or section tag.
        self.is_first_paragraph = None

        # True if italics is carried over from a previous line.
        self.is_italics = None

        # True if previous line processed was blank.
        self.is_previous_line_blank = None

        # Track state of structural markup tags.
        self.markup = MarkupState()

        self.reset()

    def _process_blank_line(self, line):
        """Update state if the line is blank.
        Lines that contain only whitespace chars are considered to be blnak.
        @type  line: str
        @param line: Proze line.
        @rtype:  bool
        @return: True if the line is blank.
        """
        if line.strip() == '':
            self.is_previous_line_blank = True
            self.is_bold = False
            self.is_italics = False
            return True
        return False

    def reset(self):
        """Reset all state values to default."""
        self.markup.reset()
        self._indent_leading_whitespace = []
        self.indent_level = 0
        self.is_bold = False
        self.is_first_paragraph = False
        self.is_italics = False
        self.is_previous_line_blank = True

    def _toggle_bold_and_italics(self, line):
        """Toggle state of bold and italics blocks that line wrap.
        @type  line: str
        @param line: Lowercase line of proze text.
        """
        if line.count('__') % 2:
            self.is_bold = not self.is_bold
        if line.count('*') % 2:
            self.is_italics = not self.is_italics

    def _update_indentation_level(self, line):
        """Update state of indented block quote paragraphs.
        @type  line: str
        @param line: Proze line.
        """
        if self.is_previous_line_blank:
            current = whitespace.match(line)
            if current:
                current = current.group(1)
                previous = ''
                if self._indent_leading_whitespace:
                    previous = self._indent_leading_whitespace[-1]
                if len(previous) > len(current):
                    self._indent_leading_whitespace.pop()
                    self.indent_level = self.indent_level - 1
                elif len(previous) < len(current):
                    self._indent_leading_whitespace.append(current)
                    self.indent_level = self.indent_level + 1
            else:
                self._indent_leading_whitespace = []
                self.indent_level = 0
        if self.indent_level < 0:
                self.indent_level = 0

    def update(self, line):
        """Update the document state based on the current line.
        @type  line: str
        @param line: Proze line.
        """
        lowercase = line.lower()
        self.is_first_paragraph = False
        self.markup.is_markup_line = False
        if not self._process_blank_line(line):
            self.markup.is_markup(lowercase, self.is_previous_line_blank)
            if self.markup.token:
                self.markup.update_structural_markup_flags(
                    self.is_previous_line_blank
                )
                if self.markup.token != MarkupToken.author:
                    self._find_first_paragraph = True
            else:
                if self._find_first_paragraph:
                    self._find_first_paragraph = False
                    self.is_first_paragraph = True
                self._toggle_bold_and_italics(lowercase)
                self._update_indentation_level(line)
                self.is_previous_line_blank = False

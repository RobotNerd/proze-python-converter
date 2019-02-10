from lib.structural_token import MarkupToken
import re

whitespace = re.compile(r'^(\s+)[^\s-]')


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

    def check_markup(self, line, previous_line):
        """Check if the line is structural markup.
        @type  line: str
        @param line: Lowercase line of proze text.
        @type  is_previous_line_blank: PreviousLine
        @param is_previous_line_blank: State of the previous line.
        """
        self.token = None
        if previous_line.is_blank or previous_line.is_structural_markup:
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

    def process_blank_line(self):
        """Update state on a blank line."""
        self.is_markup_line = False
        self.token = None

    def update_structural_markup_flags(self):
        """Update flags based on structural markup token."""
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


class PreviousLine(object):

    """State of the previous line of the proze file."""

    def __init__(self):
        # True if the line can be treated as a blank line.
        is_blank = None
        # True if the line contained a structural markup tag.
        is_structural_markup = None
        self.reset()

    def reset(self):
        self.is_blank = True
        self.is_structural_markup = False

    def update(self, is_blank, is_structural_markup):
        self.is_blank = is_blank
        self.is_structural_markup = is_structural_markup


class State(object):

    """Track current state of document compilation."""

    def __init__(self):
        # When true, the next line of proze is the first paragraph
        # after a new title, chapter, or section.
        self._find_first_paragraph = True
        # Track the indentation level for block quotes.
        self._indent_leading_whitespace = []
        self.indent_level = 0
        # True if line is blank.
        self._is_blank = None
        # True if bold is carried over from a previous line.
        self.is_bold = None
        # True if currently in the first paragraph after a title,
        # chapter, or section tag.
        self.is_first_paragraph = None
        # True if italics is carried over from a previous line.
        self.is_italics = None
        # Track state of structural markup tags.
        self.markup = MarkupState()
        # Track state of the previous line of proze.
        self.previous_line = PreviousLine()
        self.reset()

    def _process_blank_line(self):
        """Update state for a line that is blank.
        Lines that contain only whitespace chars are considered to be blank.
        """
        self._is_blank = True
        self.is_bold = False
        self.is_italics = False
        self.markup.process_blank_line()

    def _process_markup_line(self):
        """Update state for a line of structural markup."""
        self.markup.update_structural_markup_flags()
        if self.markup.token != MarkupToken.author:  # TODO check this logic
            self._find_first_paragraph = True

    def _process_proze_line(self, line, lowercase):
        """Update state for a line of proze.
        @type  line: str
        @param line: Line parsed from file.
        @type  lowercase: str
        @param lowercase: Lowercase version of the line.
        """
        if self._find_first_paragraph:
            self._find_first_paragraph = False
            self.is_first_paragraph = True
        self._toggle_bold_and_italics(lowercase)
        self._update_indentation_level(line)

    def reset(self):
        """Reset all state values to default."""
        self.markup.reset()
        self.previous_line.reset()
        self._indent_leading_whitespace = []
        self.indent_level = 0
        self._is_blank = True
        self.is_bold = False
        self.is_first_paragraph = False
        self.is_italics = False

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
        if self.previous_line.is_blank:
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
        self.previous_line.update(self._is_blank, self.markup.is_markup_line)
        if line.strip() == '':
            self._process_blank_line()
        else:
            self._is_blank = False
            self.markup.check_markup(lowercase, self.previous_line)
            if self.markup.token:
                self._process_markup_line()
            else:
                self._process_proze_line(line, lowercase)

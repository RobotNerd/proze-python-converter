from lib.rules import Rules
from lib.structural_token import MarkupToken
from strategy.base import BaseStrategy, BaseStrategyCompiler
import re

MAX_LINE_LENGTH = 80


class TextStrategy(BaseStrategy):

    """Compile to a plain text file."""

    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        self.options = options

    def compile(self, path):
        """Compile the project.
        @type  path: str
        @param path: Path of the output file to be generated.
        @rtype: _TextStrategyCompiler
        @return: Compilation object that can be used in a 'with' clause.
        """
        return _TextStrategyCompiler(path, self.options)


class _TextStrategyCompiler(BaseStrategyCompiler):

    """Compile to a plain text file."""

    def __init__(self, path, options):
        """Constructor.
        @type  path: str
        @param path: Path of output file to be generated.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        self.handle = None
        self.options = options
        self.path = path
        self.rules = Rules(options)

    def __enter__(self):
        """Create and open a new document."""
        self.handle = open(self.path, 'w')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the open file handle."""
        self.handle.close()

    def _blank_lines(self, state):
        """Determine the number of blank lines to insert before this one.
        :param lib.state.State state: Formatting state of current line of text.
        :return str: Line breaks to add as a prefix to the current line.
        """
        blank_lines = ''
        if state.is_first_paragraph:
            if state.markup.is_chapter or state.markup.is_section:
                blank_lines = '\n'
            else:
                blank_lines = '\n\n'
        elif state.markup.token:
            if (
                state.markup.token == MarkupToken.chapter or
                state.markup.token == MarkupToken.section
            ):
                blank_lines = '\n\n'
            elif state.markup.token == MarkupToken.section_break:
                blank_lines = '\n'
        return blank_lines

    def _format(self, line, state):
        """Format the line of text for the target document type.
        @type  line: str
        @param line: Proze formatted line to be written to the document.
        @type  state: lib.state.State
        @param state: Formatting state of the current line of text.
        @rtype:  str
        @return: Formatted line for insertion into the document.
        """
        line = self.rules.clean_whitespace(line)
        blank_lines = self._blank_lines(state)
        if state.markup.is_markup_line:
            line = blank_lines + self._parse_structural_markup(line, state)
        else:
            first_char = self.rules.first_character(state, use_spaces=True)
            line = blank_lines + first_char + line
            line = self._strip_bold_italics(line)
        return line

    def _parse_structural_markup(self, line, state):
        """Process lines of structural markup.
        @type  line: str
        @param line: Proze formatted line to be written to the document.
        @type  state: lib.state.State
        @param state: Formatting state of the current line of text.
        @rtype:  str
        @return: Line after structural markup changes are applied.
        """
        if state.markup.token == MarkupToken.author:
            line = re.sub(state.markup.token, 'by', line, flags=re.I)
        elif state.markup.token == MarkupToken.chapter:
            line = re.sub(state.markup.token, '', line, flags=re.I)
        elif state.markup.token == MarkupToken.section:
            line = re.sub(state.markup.token, '', line, flags=re.I)
        elif state.markup.token == MarkupToken.section_break:
            line = line.strip()
        elif state.markup.token == MarkupToken.title:
            line = re.sub(state.markup.token, '', line, flags=re.I)
        return line.strip()

    def _split_on_line_length(self, line):
        """Split into multiple lines if longer than MAX_LINE_LENGTH.
        @type  line: str:
        @param line: Text to be split.
        @rtype:  list
        @return: Split line.
        """
        lines = []
        curr = line
        while len(curr) > MAX_LINE_LENGTH:
            index = MAX_LINE_LENGTH
            while curr[index] not in [' ', '-'] and index >= 0:
                index -= 1
            if index == 0:
                # Force a hard mid-word split for really long words.
                index = MAX_LINE_LENGTH
            lines.append(curr[0:index])
            curr = curr[index+1:]
        lines.append(curr)
        return lines

    def _strip_bold_italics(self, line):
        """Remove bold and italic markup.
        @type  line: str
        @param line: Proze formatted line to be written to the document.
        @rtype:  str
        @return: Line after bold and italic markup is removed.
        """
        line = re.sub('\*', '', line)
        line = re.sub('__', '', line)
        return line

    def write(self, line, state):
        """Write a line of text to the output document.
        @type  line: str
        @param line: Formatted line to be written to the document.
        @type  state: lib.state.State
        @param state: Formatting state of the current line of text.
        """
        if not state.is_blank:
            line = self._format(line, state)
            lines = self._split_on_line_length(line)
            for partial in lines:
                self.handle.write(partial + '\n')

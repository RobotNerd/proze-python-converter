from lib.rules import Rules
from lib.structural_token import MarkupToken
from strategy.base import BaseStrategy, BaseStrategyCompiler
import re


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
        if state.markup.is_markup_line:
            line = self._parse_structural_markup(line, state)
        else:
            blank_lines = '\n\n' if state.is_first_paragraph else ''
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
            pass
        elif state.markup.token == MarkupToken.section:
            line = re.sub(state.markup.token, '', line, flags=re.I)
        elif state.markup.token == MarkupToken.section_break:
            line = line.strip()
        elif state.markup.token == MarkupToken.title:
            line = re.sub(state.markup.token, '', line, flags=re.I)
        return line.strip()

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
            self.handle.write(line + '\n')

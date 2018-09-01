from base import BaseStrategy, BaseStrategyCompiler
from lib.rules import Rules
import re


class TextStrategy(BaseStrategy):

    """Compile to a plain text file."""

    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        self.options = options

    def compile(self):
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

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the open file handle."""
        self.handle.close()

    # TODO replace kwargs by creating a state object
    def _format(self, line, **kwargs):
        """Format the line of text for the target document type.
        @type  line: str
        @param line: Proze formatted line to be written to the document.
        @param kwargs: Formatting state flags applied to this line of text.
            - bold: If True, bold is applied from the previous line.
            - italics: If True, italics is applied from the previous line.
            - is_first_paragraph: True if this is the first paragraph in
                the current chapter or section.
            - is_previous_line_blank: True if previous line in the proze
                file contains only whitespace.
        @return: Formatted line for insertion into the document.
        """
        line = self.rules.clean_whitespace(line)
        line = self.rules.first_character(**kwargs) + line
        line = self._strip_bold_italics(line)
        # TODO remove markup tags (Title, Chapter, etc)
        return line

    def _strip_bold_italic(self, line):
        """Remove bold and italic markup.
        @type  line: str
        @param line: Proze formatted line to be written to the document.
        @rtype:  str
        @return: Line after bold and italic markup is removed.
        """
        line = re.sub('*', '', line)
        line = re.sub('__', '', line)
        return line

    def write(self, line):
        """Write a line of text to the output document.
        @param line: Formatted line to be written to the document.
        """
        self.handle.write(line)


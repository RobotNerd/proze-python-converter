from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    """Base class for all document conversion strategies.

    This class is separate from the actual converter class so that
    the strategy can be chosen without triggering the __enter__
    method.
    """

    @abstractmethod
    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        pass

    @abstractmethod
    def compile(self, path):
        """Compile the project.
        @type  path: str
        @param path: Path of the output file to be generated.
        @rtype:  BaseStrategyConverter
        @return: Compilation object that can be used in a 'with' clause.
        """
        pass


class BaseStrategyCompiler(ABC):

    """Base class for all compilers that can be used in a 'with' clause."""

    @abstractmethod
    def __init__(self, path, options):
        """Constructor.
        @type  path: str
        @param path: Path of output file to be generated.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        pass

    @abstractmethod
    def __enter__(self):
        """Create and open a new document."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """Close the open file handle."""
        pass

    @abstractmethod
    def _format(self, line, **kwargs):
        """Format the line of text for the target document type.
        @type  line: str
        @param line: Prose formatted line to be written to the document.
        @param kwargs: Formatting state flags applied to this line of text.
            - bold: If True, bold is applied from the previous line.
            - italics: If True, italics is applied from the previous line.
            - is_first_paragraph: True if this is the first paragraph in
                the current chapter or section.
        @return: Formatted line for insertion into the document.
        """
        pass

    @abstractmethod
    def write_line(self, line):
        """Write a line of text to the output document.
        @type  line: str
        @param line: Formatted line to be written to the document.
        """
        pass

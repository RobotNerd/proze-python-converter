import re


class Names(object):

    """Work with character names in proze documents."""

    # Include negative lookahead/lookbehind to prevent matching
    # against invalid name patterns that are part of a larger word.
    invalid_base = '(?<![0-9a-zA-Z_-]){}(?![0-9a-zA-Z_-])'

    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Config options that contain character names.
        """
        self.options = options
        self.invalid_patterns = {}  # Cache compiled invalid name regexs

    def find_invalid(self, line):
        """Find all invalid character names on the line.
        @type  line: str
        @param line: Proze formatted line.
        @rtype:  list
        @return: List of all invalid character names found on the line.
        """
        found = []
        line = line.lower()
        if self.options.names.invalid:
            for invalid in self.options.names.invalid:
                key = invalid.lower()
                pattern = self.invalid_patterns.get(key)
                if pattern is None:
                    pattern = re.compile(self.invalid_base.format(key))
                    self.invalid_patterns[key] = pattern
                if pattern.search(line) is not None:
                    found.append(invalid)
        return found

import re

OPEN = '['
CLOSE = ']'


class Brackets(object):

    """Remove brackets from proze lines."""

    def __init__(self):
        # Keep track of being in a bracket block.
        self.in_bracket_block = False

    def _next_token(self, line):
        """Get the index of the next open/close bracket on the line.
        @type  line: str
        @param line: The proze line being processed.
        @rtype:  tuple(int, str)
        @return: Bracket index, bracket type. Both None if no bracket found.
        """
        token = CLOSE if self.in_bracket_block else OPEN
        try:
            index = line.index(token)
        except ValueError:
            index = None
            token = None
        return index, token

    def remove(self, line):
        """Remove bracket blocks from the line.
        @type  line: str
        @param line: proze formatted line.
        @rtype:  str
        @return: proze formatted line with bracketed blocks removed.
        """
        result = ''
        right = line
        while right:
            index, token = self._next_token(right)
            if index is not None:
                left = right[0:index]
                right = right[index+1:len(right)]
                if not self.in_bracket_block:
                    # Starting new block, continue parsing right.
                    self.in_bracket_block = True
                    result = result + left
                else:
                    # Closing existing block, discard left.
                    self.in_bracket_block = False
            else:
                if not self.in_bracket_block:
                    result = result + right
                right = None
        return result

    def reset(self):
        """Clear state values."""
        self.in_bracket_block = False

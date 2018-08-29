import re

BLOCK_TOKEN = '###'
LINE_TOKEN = '##'


class Comments(object):

    """Remove comments from proze lines."""

    def __init__(self):
        # Keep track of being in an open comment block.
        self._in_comment_block = False

    def _next_token(self, line):
        """Get the index and type of the first occurrence of a comment token.
        @type  line: str
        @param line: The proze line being processed.
        @rtype:  tuple(int, str)
        @return: Line token index, value. Both None if no comment token found.
        """
        if self._in_comment_block:
            # If this is part of an already opened block token, then
            # the next line token can be ignored. Only the closing block
            # token will matter.
            index_line = None
        else:
            try:
                index_line = line.index(LINE_TOKEN)
            except ValueError:
                index_line = None
        try:
            index_block = line.index(BLOCK_TOKEN)
        except ValueError:
            index_block = None
        index = None
        token = None
        if index_line is None:
            if index_block is not None:
                index = index_block
                token = BLOCK_TOKEN
        elif index_block is not None:
            if index_block <= index_line:
                index = index_block
                token = BLOCK_TOKEN
            else:
                index = index_line
                token = LINE_TOKEN
        else:
            index = index_line
            token = LINE_TOKEN
        return index, token

    def remove(self, line):
        """remove comment blocks from the line.
        @type  line: str
        @param line: proze formatted line.
        @rtype:  str
        @return: proze formatted line with comments removed.
        """
        result = ''
        right = line
        while right:
            index, token = self._next_token(right)
            if index is not None:
                if token == BLOCK_TOKEN:
                    left, right = right.split(BLOCK_TOKEN, 1)
                    if not self._in_comment_block:
                        result = result + left
                    self._in_comment_block = not self._in_comment_block
                else:
                    keep, _ = right.split(token, 1)
                    right = None
                    result = result + keep
            else:
                if not self._in_comment_block:
                    result = result + right
                right = None
        return result.strip()

    def reset(self):
        """Clear state values."""
        self._in_comment_block = False

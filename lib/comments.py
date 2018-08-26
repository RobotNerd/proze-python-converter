import re


class Comments(object):

    """Remove comments from proze lines."""

    def __init__(self):
        # Used to keep track of open comment blocks that can span
        # multiple lines.
        self._in_comment_block = False

    def remove(self, line):
        """Remove comment blocks from the line.
        @type  line: str
        @param line: Proze formatted line.
        @rtype:  str
        @return: Proze formatted line with comments removed.
        """
        # TODO if currently in a comment block, look for the end of the
        #   block or comment out then entire line
        raise NotImplementedError

    def reset(self):
        """Clear state values."""
        self._in_comment_block = False



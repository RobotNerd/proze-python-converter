import re

BLOCK_TOKEN = '###'
LINE_TOKEN = '##'
BRACKET_OPEN = '['
BRACKET_CLOSE = ']'


class RegexNotFound(Exception):
    pass


class Blocks(object):

    """Strip comments and bracket blocks from lines."""

    def __init__(self):
        self.in_bracket_block = False
        self.in_comment_block = False
        self._regex = self._compile_regex()

    def _compile_regex(self):
        """Precompute regex patterns for each token type.
        The pattern matches the first non-escaped token on the line.
        @rtype:  dict
        @return: Regex patterns to find first occurrence of a token.
        """
        result = {}
        tokens = [ BLOCK_TOKEN, LINE_TOKEN, BRACKET_CLOSE ]
        escape_tokens = [ BRACKET_OPEN ]
        for token in tokens:
            result[token] = re.compile(r'^.*?(?<!\\)({})'.format(token))
        for token in escape_tokens:
            result[token] = re.compile(r'^.*?(?<!\\)(\{})'.format(token))
        return result

    def _get_index(self, line, token):
        """Get index of first occurrence of the token in the string.
        @type  line: str
        @param line: Line of proze formatted text.
        @type  token: str
        @param token: Substring being searched for.
        @rtype:  int
        @return: Index of the first token in the strong, None if not found.
        """
        index = None
        prog = self._regex.get(token)
        if prog is None:
            raise RegexNotFound('No regex found for token ' + str(token))
        match = prog.match(line)
        if match:
            index = match.start(1)
        return index

    def _next_token(self, line):
        """Get the index and type of the first comment or bracket token.
        @type  line: str
        @param line: The proze line being processed.
        @rtype:  tuple(int, str)
        @return: Line token index, value. Both None if no token found.
        """
        index = None
        token = None
        index_line_comment = self._get_index(line, LINE_TOKEN)
        index_block_comment = self._get_index(line, BLOCK_TOKEN)
        index_bracket_open = self._get_index(line, BRACKET_OPEN)
        index_bracket_close = self._get_index(line, BRACKET_CLOSE)
        if self.in_comment_block:
            # Everything is hidden up until the closing comment block token.
            index = index_block_comment
            token = BLOCK_TOKEN
        elif self.in_bracket_block:
            # Everything is hidden up until the closing bracket token.
            index = index_bracket_close
            token = BRACKET_CLOSE
        else:
            # We're looking for the first token found on the line because
            # it will hide any subsequent tokens. The closing bracket is
            # ignored because it doesn't matter in this state.
            if index_line_comment is not None:
                index = index_line_comment
                token = LINE_TOKEN
            if index_block_comment is not None:
                if not index or index_block_comment <= index:
                    index = index_block_comment
                    token = BLOCK_TOKEN
            if index_bracket_open is not None:
                if not index or index_bracket_open < index:
                    index = index_bracket_open
                    token = BRACKET_OPEN
        return index, token

    def remove(self, line):
        """Remove text from the line that is in brackets or comments.
        @type  line: str
        @param line: The proze line being processed.
        @rtype:  str
        @return: The proze formatted line with brackets/comments removed.
        """
        result = ''
        right = line
        while right:
            index, token = self._next_token(right)
            if index is not None:
                if (
                    token == BLOCK_TOKEN or
                    token == BRACKET_OPEN or
                    token == BRACKET_CLOSE
                ):
                    left, right = right[0:index], right[index+len(token):]
                    if token == BLOCK_TOKEN:
                        if not self.in_comment_block:
                            result = result + left
                        self.in_comment_block = not self.in_comment_block
                    else:
                        if not self.in_bracket_block:
                            result = result + left
                        self.in_bracket_block = not self.in_bracket_block
                else:
                    keep, _ = right[0:index], right[index:]
                    right = None
                    result = result + keep
            else:
                if not self.in_comment_block and not self.in_bracket_block:
                    result = result + right
                right = None
        return result

    def reset(self):
        """Clear state values."""
        self.in_bracket_block = False
        self.in_comment_block = False

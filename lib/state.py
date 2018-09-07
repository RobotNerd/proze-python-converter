class State(object):

    """Track current state of document compilation."""

    structural_tokens = [
        'author:',
        'chapter:',
        'section:',
        'title:',
    ]
    section_break = '---'

    def __init__(self):
        # True if bold is carried over from a previous line.
        self.is_bold = None

        # True if inside a chapter.
        self.is_chapter = None

        # True if currently in the first paragraph after a title,
        # chapter, or section tag.
        self.is_first_paragraph = None

        # When true, the next line of proze is the first paragraph
        # after a new title, chapter, or section.
        self._find_first_paragraph = True

        # True if italics is carried over from a previous line.
        self.is_italics = None

        # True if previous line processed was blank.
        self.is_previous_line_blank = None

        # True if inside a secton.
        self.is_section = None
        self.reset()

    def _is_markup(self, line):
        """Check if the line is structural markup.
        @type  line: str
        @param line: Lowercase line of proze text.
        @rtype:  str
        @return: The markup token, None if not found.
        """
        for token in self.structural_tokens:
            if line.startswith(token):
                return token
        if line.strip() == self.section_break:
            return self.section_break
        return None

    def reset(self):
        """Reset all state values to default."""
        self.is_bold = False
        self.is_chapter = False
        self.is_first_paragraph = False
        self.is_italics = False
        self.is_previous_line_blank = False
        self.is_section = False
    
    def _toggle_bold_and_italics(self, line):
        """Toggle state of bold and italics blocks that line wrap.
        @type  line: str
        @param line: Lowercase line of proze text.
        """
        if line.count('__') % 2:
            self.is_bold = not self.is_bold
        if line.count('*') % 2:
            self.is_italics = not self.is_italics

    def _update_structural_markup_flags(self, token):
        """Update flags based on structural markup token.
        @type  token: str
        @param token: Structural markup token found on the line.
        """
        if token != 'author:':
            self._find_first_paragraph = True
        if token == 'chapter:':
            self.is_chapter = True
            self.is_section = False
        elif token == 'section:' or token == self.section_break:
            self.is_chapter = False
            self.is_section = True
        else:
            self.is_chapter = False
            self.is_section = False

    def update(self, line):
        """Update the document state based on the current line.
        @type  line: str
        @param line: Proze line.
        """
        lowercase = line.lower()
        self.is_first_paragraph = False
        if not line.strip():
            self.is_previous_line_blank = True
            self.is_bold = False
            self.is_italics = False
        else:
            token = self._is_markup(lowercase)
            if token:
                self._update_structural_markup_flags(token)
            else:
                if self._find_first_paragraph:
                    self._find_first_paragraph = False
                    self.is_first_paragraph = True
                self._toggle_bold_and_italics(lowercase)

class State(object):

    """Track current state of document compilation."""

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

    def reset(self):
        """Reset all state values to default."""
        self.is_bold = False
        self.is_chapter = False
        self.is_first_paragraph = False
        self.is_italics = False
        self.is_previous_line_blank = False
        self.is_section = False
    
    def _starts_new_part(self, line):
        """Check if the line starts a new title, chapter, or section.
        @type  line: str
        @param line: Proze line.
        @rtype:  bool
        @return: True if the line starts a title, chapter, or section.
        """
        starts_new = False
        lowercase = line.lower()
        if lowercase.startswith('title:'):
            self.is_chapter = False
            self.is_section = False
            self._find_first_paragraph = True
            starts_new = True
        elif lowercase.startswith('chapter:'):
            self.is_chapter = True
            self.is_section = False
            self._find_first_paragraph = True
            starts_new = True
        elif lowercase.startswith('section:') or lowercase.strip() == '---':
            self.is_chapter = False
            self.is_section = True
            self._find_first_paragraph = True
            starts_new = True
        return starts_new

    def update(self, line):
        """Update the document state based on the current line.
        @type  line: str
        @param line: Proze line.
        """
        self.is_first_paragraph = False
        if not line.strip():
            self.is_previous_line_blank = True
        elif not self._starts_new_part(line):
            if self._find_first_paragraph:
                self._find_first_paragraph = False
                self.is_first_paragraph = True

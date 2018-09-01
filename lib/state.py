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

    def update(self, line):
        """Update the document state based on the current line.
        @type  line: str
        @param line: Proze line.
        """
        # TODO check if a tag block (title, section, chapter, author, etc)
        #   and set first paragraph, is_chapter, etc. accordingly
        # TODO check if the line is blank
        raise NotImplementedError

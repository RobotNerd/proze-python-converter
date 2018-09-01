class State(object):

    """Track current state of document compilation."""

    def __init__(self):
        # True if inside a chapter.
        self.is_chapter = False

        # True if currently in the first paragraph after a title,
        # chapter, or section tag.
        self.is_first_paragraph = False

        # True if previous line processed was blank.
        self.is_previous_line_blank = False

        # True if inside a secton.
        self.is_section = False

    def reset(self):
        """Reset all state values to default."""
        self.is_chapter = False
        self.is_first_paragraph = False
        self.is_previous_line_blank = False
        self.is_section = False

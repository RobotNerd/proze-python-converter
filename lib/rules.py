import re

# Number of spaces to use per tab.
SPACES_PER_TAB = 4


class Rules(object):

    """Formatting rules."""

    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Compile options parsed from the config file.
        """
        self.options = options

    def clean_whitespace(self, line):
        """Clean up whitespce on the line.
        @type  line: str
        @param line: Proze formatted line of text.
        @rtype:  str
        @return: Line with properly formatted whitespace.
        """
        line = line.strip()
        return re.sub(r'\s+', ' ', line)

    def first_character(self, state, use_spaces=False):
        """Get character(s) to insert at the beginning of the paragraph.
        It can be an empty string if no characters should be inserted.

        @type  state: lib.state.State
        @param state: Current state of document compilation.
        @type  use_spaces: bool
        @param use_spaces: If True, return spaces instead of tabs.
        @rtype:  str
        @return: Characters to be inserted.
        """
        to_insert = ''
        add_tab = False
        if self.options.compile.paragraph.mode == 'prose':
            add_tab = True
            if not state.previous_line.is_blank:
                add_tab = False
            elif state.is_first_paragraph:
                add_tab = False
                if (
                    state.markup.is_chapter and
                    self.options.compile.paragraph.tabFirst.chapter
                ):
                    add_tab = True
                elif (
                    state.markup.is_section and
                    self.options.compile.paragraph.tabFirst.section
                ):
                    add_tab = True
                elif self.options.compile.paragraph.tabFirst.title:
                    add_tab = True
        if add_tab:
            if use_spaces:
                to_insert = " " * SPACES_PER_TAB
            else:
                to_insert = "\t"
        return to_insert

import re

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

    def first_character(self, **kwargs):
        """Character(s) to insert at the beginning of the paragraph.
        It can be an empty string if no characters should be inserted.
        @type  kwargs: dict
        @param kwargs: Formatting state flags applied to this line of text.
        @rtype:  str
        @return: Characters to be inserted.
        """
        to_insert = ''
        add_tab = False
        if kwargs.get('is_previous_line_blank'):
            add_tab = True
        elif kwargs.get('is_first_paragraph'):
            if self.options.paragraph.tabFirstParagraph == 'always':
                add_tab = True
            elif self.options.paragraph.tabFirstParagraph == 'chapter':
                if kwargs.get('is_chapter'):
                    add_tab = True
            elif self.options.paragraph.tabFirstParagraph == 'section':
                if kwargs.get('is_section'):
                    add_tab = True
        if add_tab:
            to_insert = "\t"
        return to_insert


class Names(object):

    """Work with character names in proze documents."""

    def __init__(self, options):
        """Constructor.
        @type  options: DotMap
        @param options: Config options that contain character names.
        """
        self.options = options

    def find_invalid(self, line):
        """Find all invalid character names on the line.
        @type  line: str
        @param line: Proze formatted line.
        @rtype:  list
        @return: List of all invalid character names found on the line.
        """
        raise NotImplementedError


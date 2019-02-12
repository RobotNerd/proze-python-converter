class MockArgs(object):

    """Mock for command line args."""

    def __init__(self, **kwargs):
        self.doctype = kwargs.get('doctype')
        self.output = kwargs.get('output')
        self.path = kwargs.get('path')


class NameOptions(object):

    """Mock of configurable names."""

    def __init__(self):
        self.characters = []
        self.places = []
        self.things = []
        self.invalid = []


class MockOptions(object):

    """Mock of options parsed from config."""

    def __init__(self):
        self.names = NameOptions()

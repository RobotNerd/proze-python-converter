from collections import namedtuple

# Note: For Python < 3.7, namedtuples don't support default values
# as part of the constructor. The code below uses a workaround based
# on https://stackoverflow.com/a/18348004/241025.


# Mock of command line arguments
MockArgs = namedtuple('MockArgs', ['doctype', 'output', 'path'])
MockArgs.__new__.__defaults__ = (None, None, None)

# MockOptions = namedtuple('MockOptions', ['names'])
# MockNames = namedtuple(
#     'MockNames',
#     ['characters', 'places', 'things', 'invalid']
# )
# MockNames.__new__.__defaults__ = (None, None, None, None)


class NameOptions(object):
    def __init__(self):
        self.characters = []
        self.places = []
        self.things = []
        self.invalid = []


class MockOptions(object):
    def __init__(self):
        self.names = NameOptions()

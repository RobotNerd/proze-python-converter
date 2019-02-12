from collections import namedtuple

# Mock of command line arguments
MockArgs = namedtuple('MockArgs', ['doctype', 'output', 'path'])
MockArgs.__new__.__defaults__ = (None, None, None)

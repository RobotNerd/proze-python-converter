from dotmap import DotMap
import lib.config
import os
import proze
import unittest

PATH = 'test/sample/tmp/output.txt'


class TestEmpty(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(PATH)
        except OSError:
            pass

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = PATH[:-4]
        args.path = 'test/sample/no_data'
        proze.run(args)
        self.assertFalse(os.path.isfile(PATH))


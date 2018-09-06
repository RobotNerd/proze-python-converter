from dotmap import DotMap
import lib.config
import os
import proze
import unittest


class TestEmpty(unittest.TestCase):

    def test_compile_empty(self):
        """A project with no config/proze files generates nothing."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = 'test/sample/tmp/output'
        args.path = 'test/sample/no_data'
        proze.run(args)
        self.assertFalse(os.path.isfile(args.output + '.txt'))


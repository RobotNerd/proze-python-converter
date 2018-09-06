from dotmap import DotMap
import lib.config
import os
import proze
import unittest


class TestCompileMissing(unittest.TestCase):

    def test_compile_missing(self):
        """A project config file has links to files that don't exist."""
        args = DotMap()
        args.doctype = 'txt'
        args.output = 'test/sample/tmp/output'
        args.path = 'test/sample/missing_data'
        proze.run(args)
        with open(args.output + '.txt') as f:
            self.assertEqual(f.read(), '')


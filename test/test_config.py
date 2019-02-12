from test.mock import MockArgs
import lib.config
import unittest

dark_and_stormy = 'test/sample/dark-and-story'
feelings = 'test/sample/feelings'
no_data = 'test/sample/no_data'


class TestConfigLoader(unittest.TestCase):

    def test_compile_options(self):
        """Test loading compile options from config file."""
        args = MockArgs(path=dark_and_stormy)
        options = lib.config.load(args)
        self.assertEqual(options.compile.paragraph.mode, 'prose')
        self.assertFalse(options.compile.paragraph.tabFirst.title)
        self.assertTrue(options.compile.paragraph.tabFirst.chapter)
        self.assertTrue(options.compile.paragraph.tabFirst.section)
        self.assertFalse(options.compile.paragraph.removeBlankLines)
        self.assertEqual(options.compile.spacing, 'double')

    def test_names(self):
        """Test names loaded from config file."""
        characters = [
            'Dallas',
            'Jacob',
            'Kathy Jones',
            'Sally',
            'Winchester Mason',
        ]
        places = ['Happenstance Ridge', 'Tottle Town']
        things = ['cheddar house', 'quick zapper']
        invalid = [
            'cheddar castle',
            'Gerald',
            'Happenstance Plateau',
            'Yates',
        ]
        args = MockArgs(path=dark_and_stormy)
        options = lib.config.load(args)
        self.assertEqual(options.names.characters, characters)
        self.assertEqual(options.names.places, places)
        self.assertEqual(options.names.things, things)
        self.assertEqual(options.names.invalid, invalid)

    def test_no_data(self):
        """Test a project path that doesn't have a config nor proze files."""
        args = MockArgs(path=no_data)
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, [])
        self.assertEqual(options.names.characters, [])
        self.assertEqual(options.names.places, [])
        self.assertEqual(options.names.things, [])
        self.assertEqual(options.names.invalid, [])

        # Default compile options should be used.
        self.assertEqual(options.compile.paragraph.mode, 'prose')
        self.assertFalse(options.compile.paragraph.tabFirst.title)
        self.assertFalse(options.compile.paragraph.tabFirst.chapter)
        self.assertFalse(options.compile.paragraph.tabFirst.section)
        self.assertTrue(options.compile.paragraph.removeBlankLines)
        self.assertEqual(options.compile.spacing, 'single')

    def test_order_from_config(self):
        """Test order of files based on config file."""
        order = [
            'title.proze',
            'erased.proze',
            'disaster.proze',
            'flee.proze',
            'reassurances.proze',
            'awakening.proze',
        ]
        args = MockArgs(path=dark_and_stormy)
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, order)

    def test_order_no_config(self):
        """Test globbing files for the file order if not in the config file."""
        order = [
            'conflict/cruise/bridge.proze',
            'conflict/cruise/cabin.proze',
            'conflict/cruise/deck.proze',
            'conflict/cruise/engine-room.proze',
            'conflict/dinner-party.proze',
            'conflict/forest.proze',
            'conflict/shopping.proze',
            'romance/at-the-lake.proze',
            'romance/blimp.proze',
            'romance/caverns.proze',
            'romance/rainstorm.proze',
            'title.proze',
        ]
        args = MockArgs(path=feelings)
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, order)

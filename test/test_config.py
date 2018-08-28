from dotmap import DotMap
import lib.config
import unittest

paths = DotMap()
paths.dark_and_stormy = 'test/sample/dark-and-story'
paths.feelings = 'test/sample/feelings'
paths.no_data = 'test/sample/no_data'


class TestConfigLoader(unittest.TestCase):

    def test_compile_options(self):
        """Test loading compile options from config file."""
        args = DotMap()
        args.path = paths.dark_and_stormy
        options = lib.config.load(args)
        self.assertEqual(options.compile.paragraph.tabFirstParagraph, 'always')
        self.assertEqual(options.compile.paragraph.removeBlankLines, 'never')
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
        args = DotMap()
        args.path = paths.dark_and_stormy
        options = lib.config.load(args)
        self.assertEqual(options.names.characters, characters)
        self.assertEqual(options.names.places, places)
        self.assertEqual(options.names.things, things)
        self.assertEqual(options.names.invalid, invalid)

    def test_no_data(self):
        """Test a project path that doesn't have a config nor proze files."""
        args = DotMap()
        args.path = paths.no_data
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, [])
        self.assertEqual(options.names.characters, [])
        self.assertEqual(options.names.places, [])
        self.assertEqual(options.names.things, [])
        self.assertEqual(options.names.invalid, [])

    def test_order_from_config(self):
        """Test globbing files based on config file."""
        order = [
            'title.proze',
            'erased.proze',
            'disaster.proze',
            'flee.proze',
            'reassurances.proze',
            'awakening.proze',
        ]
        args = DotMap()
        args.path = paths.dark_and_stormy
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, order)

    def test_order_no_config(self):
        """Test globbing files for the file order if not in the config file."""
        order = [
            'test/sample/feelings/conflict/cruise/bridge.proze',
            'test/sample/feelings/conflict/cruise/cabin.proze',
            'test/sample/feelings/conflict/cruise/deck.proze',
            'test/sample/feelings/conflict/cruise/engine-room.proze',
            'test/sample/feelings/conflict/dinner-party.proze',
            'test/sample/feelings/conflict/forest.proze',
            'test/sample/feelings/conflict/shopping.proze',
            'test/sample/feelings/romance/at-the-lake.proze',
            'test/sample/feelings/romance/blimp.proze',
            'test/sample/feelings/romance/caverns.proze',
            'test/sample/feelings/romance/rainstorm.proze',
            'test/sample/feelings/title.proze',
        ]
        args = DotMap()
        args.path = paths.feelings
        options = lib.config.load(args)
        self.assertEqual(options.compile.order, order)

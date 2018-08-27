"""Parse prose config file."""
from dotmap import DotMap
import json
import os
import yaml


def _default(args):
    """Get data struct containing default options.
    @type  args: object
    @param args: Command line arguments.
    @rtype:  DotMap
    @return: Default options.
    """
    options = DotMap()
    options.names.characters = []
    options.names.places = []
    options.names.things = []
    options.names.invalid = []
    options.compile.order = _find_proze_files(args)
    options.compile.paragraph.tabFirstParagraph = 'never'
    options.compile.paragraph.removeBlankLines = 'always'
    options.compile.spacing = 'single'
    return options


def _find_config_path(args):
    """Find the path to the proze config file.
    @type  args: object
    @param args: Command line arguments.
    @rtype:  str
    @return: Path to config file if found. None otherwise.
    """
    filenames = ['config.json', 'config.yml', 'config.yaml']
    if args.path:
        for name in filenames:
            path = args.path + '/' + name
            if os.path.is_file(path):
                return path
    else:
        cwd = os.getcwd()
        for name in filenames:
            path = cwd + '/' + name
            if os.path.is_file(path):
                return path
    return None


def _find_proze_files(args):
    """Find proze files and build a default compile order.
    @type  args: object
    @param args: Command line arguments.
    @rtype:  list
    @return: Paths to proze files found.
    """
    # TODO args.path contains target proze directory
    if args.path:
        pass
    else:
        cwd = os.getcwd()
    raise NotImplementedError


def load(args):
    """Load proze configuration file.
    @type  args: object
    @param args: Command line arguments.
    @rtype:  DotMap
    @return: Options parsed from the project config file. Default options
        if no config file is found.
    """
    options = _default(args)
    path = _find_config_path(args)
    if not path:
        print('No config file found for project. Using default settings.')
    else:
        _parse_config(path, options)
    return options


def _parse_config(path, options):
    """Parse options from the config file.
    @type  path: str
    @param path: Path to the config file.
    @type  options: DotMap
    @param options: Object loaded with default options. Parsed options
        are inserted into here.
    """
    with open(path, 'r') as conf:
        ext = os.path.splitext(path)[1]
        if ext == 'json':
            parsed = json.loads(conf.read())
        elif ext == 'yaml':
            parsed = yaml.safe_load(conf)
        else:
            raise TypeError('Unrecognized config file type: {}'.format(ext))
        if parsed:
            _parse_compile_options(parsed, options)
            _parse_names(parsed, options)


def _parse_compile_options(parsed, options):
    """Parse compile options from the config file data.
    @type  parsed: object
    @param parsed: Data loaded from the config file.
    @type  options: DotMap
    @param options: Data structure where options are stored.
    """
    _parse_compile_order(parsed, options)
    _parse_paragraph_options(parsed, options)
    _parse_spacing(parsed, options)


def _parse_compile_order(parsed, options):
    """Parse the order in which proze files are processed.
    @type  parsed: object
    @param parsed: Data loaded from the config file.
    @type  options: DotMap
    @param options: Data structure where options are stored.
    """
    compiler = parsed.get('compile')
    if compiler:
        order = order.get('order')
        if order:
            options.compile.order = order


def _parse_names(parsed, options):
    """Parse names from the config file data.
    @type  parsed: object
    @param parsed: Data loaded from the config file.
    @type  options: DotMap
    @param options: Data structure where options are stored.
    """
    names = parsed.get('names')
    if names:
        if names.get('characters'):
            options.names.characters = names.get('characters')
        if names.get('places'):
            options.names.places = names.get('places')
        if names.get('things'):
            options.names.things = names.get('things')
        if names.get('invalid'):
            options.names.invalid = names.get('invalid')


def _parse_paragraph_options(parsed, options):
    """Parse compile options for paragraph formatting.
    @type  parsed: object
    @param parsed: Data loaded from the config file.
    @type  options: DotMap
    @param options: Data structure where options are stored.
    """
    valid_blank = ['always', 'never']
    valid_tab = ['always', 'chapter', 'never', 'section']
    compiler = parsed.get('compile')
    if compiler:
        paragraph = compiler.get('paragraph')
        if paragraph:
            blank = paragraph.get('removeBlankLines')
            if blank:
                blank = blank.lower()
                if blank in valid_blank:
                    options.compile.paragraph.removeBlankLines = blank
            tab = paragraph.get('tabFirstParagraph')
            if tab:
                tab = tab.lower()
                if tab in valid_tab:
                    options.compile.paragraph.tabFirstParagraph = tab


def _parse_spacing(parsed, options):
    """Parse compile option for line spacing.
    @type  parsed: object
    @param parsed: Data loaded from the config file.
    @type  options: DotMap
    @param options: Data structure where options are stored.
    """
    valid = ['single', 'single+', 'double']
    compiler = parsed.get('compile')
    if compiler:
        spacing = compiler.get('spacing')
        if spacing:
            spacing = spacing.lower()
            if spacing in valid:
                options.compile.spacing = spacing

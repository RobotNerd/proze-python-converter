"""Parse prose config file."""
from dotmap import DotMap
import glob
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
    options.compile.paragraph.mode = 'prose'
    options.compile.paragraph.removeBlankLines = True
    options.compile.paragraph.tabFirst.chapter = False
    options.compile.paragraph.tabFirst.section = False
    options.compile.paragraph.tabFirst.title = False
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
            if os.path.isfile(path):
                return path
    else:
        cwd = os.getcwd()
        for name in filenames:
            path = cwd + '/' + name
            if os.path.isfile(path):
                return path
    return None


def _find_proze_files(args):
    """Find proze files and build a default compile order.
    @type  args: object
    @param args: Command line arguments.
    @rtype:  list
    @return: Paths to proze files found.
    """
    root = args.path if args.path else cwd.getcwd()
    proze_files = sorted(
        glob.glob(root + '/**/*.proze', recursive=True)
    )
    # Strip the base path from the glob patterns.
    # Add one to root length to account for extra '/' character.
    proze_files = [x[len(root) + 1:] for x in proze_files]
    return proze_files


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
        if path.endswith('json'):
            parsed = json.loads(conf.read())
        elif path.endswith('yaml') or path.endswith('yml'):
            parsed = yaml.safe_load(conf)
        else:
            raise TypeError('Unrecognized config file type: {}'.format(path))
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
        order = compiler.get('order')
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
    valid_modes = ['justified', 'prose']
    compile_opts = parsed.get('compile')
    if compile_opts:
        paragraph = compile_opts.get('paragraph')
        if paragraph:
            options.compile.paragraph.removeBlankLines = _validate_bool(
                paragraph.get('removeBlankLines'),
                options.compile.paragraph.removeBlankLines
            )
            options.compile.paragraph.mode = _validate_string(
                paragraph.get('mode'),
                valid_modes,
                options.compile.paragraph.mode
            )
            tabFirst = paragraph.get('tabFirst')
            if tabFirst:
                options.compile.paragraph.tabFirst.chapter = _validate_bool(
                    tabFirst.get('chapter'),
                    options.compile.paragraph.tabFirst.chapter
                )
                options.compile.paragraph.tabFirst.title = _validate_bool(
                    tabFirst.get('title'),
                    options.compile.paragraph.tabFirst.title
                )
                options.compile.paragraph.tabFirst.section = _validate_bool(
                    tabFirst.get('section'),
                    options.compile.paragraph.tabFirst.section
                )


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


def _validate_bool(value, default):
    """Validate a boolean value parsed from the config file.
    @type  value: any
    @param value: Raw value read from config.
    @type  default: bool
    @param default: Default value to use if the input value isn't valid.
    @rtype:  bool
    @return: Value to use.
    """
    if value is not None:
        if type(value) is bool:
            return value
    return default


def _validate_string(value, valid_values, default):
    """Validate a string value parsed from the config file.
    @type  value: str
    @param value: Raw value read from config.
    @type  valid_values: list
    @param valid_values: Allowed values.
    @type  default: str
    @param default: Default value to use if the input value isn't valid.
    @rtype:  str
    @return: Value to use.
    """
    if value:
        value = value.lower()
        if value in valid_values:
            return value
    return default

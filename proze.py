#!/usr/bin/python3
from lib.blocks import Blocks
from lib.names import Names
from lib.state import State
from strategy.text import TextStrategy
import lib.cli
import lib.config
import os


class StrategyNotFoundError(Exception):
    pass


def check_invalid_names(line, path, line_number, names):
    """Check the line and warn if it contains invalid names.
    @type  line: str
    @param line: Proze formatted line.
    @type  path: str
    @param path: Path to the proze file being parsed.
    @type  line_number: number
    @param line_number: Current line number in the file being parsed.
    @type  names: lib.names.Names
    @param names: Methods for managing character names.
    """
    invalid = names.find_invalid(line)
    if invalid:
        print(
            'WARN: Invalid names found in {}[{}]: {}'.format(
                path, line_number, invalid
            )
        )


def determine_strategy(args, options):
    """Determine the strategy to use when compiling the document.
    @type  args: object
    @param args: Parsed command line args.
    @type  options: DotMap
    @param options: Compile options parsed from the config file.
    @rtype:  BaseStrategy
    @return: Strategy to use.
    """
    if args.doctype == 'pdf':
        raise NotImplementedError
    elif args.doctype == 'txt':
        return TextStrategy(options)
    raise StrategyNotFoundError(
        'Unrecognized strategy {}'.format(args.doctype)
    )


def execute_strategy(strategy, args, options):
    """Compile the proze project using the strategy.
    @type  strategy: BaseStrategy
    @param strategy: Strategy to use.
    @type  args: object
    @param args: Parsed command line args.
    @type  options: DotMap
    @param options: Compile options parsed from the config file.
    """
    blocks = Blocks()
    names = Names(options)
    state = State()
    output_path = args.output + '.' + args.doctype
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with strategy.compile(output_path) as compiler:
        for filename in options.compile.order:
            path = args.path + '/' + filename
            try:
                with open(path, 'r') as proze_file:
                    blocks.reset()
                    state.reset()
                    line_number = 0
                    for raw_line in proze_file:
                        line_number = line_number + 1
                        line = blocks.remove(raw_line)
                        check_invalid_names(line, path, line_number, names)
                        if line:
                            compiler.write(line, state)
                        # TODO parsed or raw version of line?
                        state.update(raw_line)
            except FileNotFoundError:
                print(
                    'MISSING: Cannot find file "{}". '.format(path) +
                    'Update the file names in your config file.'
                )


def run(args):
    """Compile proze to target format.
    @type  args: object
    @param args: Parsed command line args.
    """
    options = lib.config.load(args)
    if not options.compile.order:
        print('No proze files to compile.')
    else:
        strategy = determine_strategy(args, options)
        execute_strategy(strategy, args, options)


if __name__ == "__main__":
    args = lib.cli.parse()
    run(args)

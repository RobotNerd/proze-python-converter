#!/usr/bin/python3
from lib.comments import Comments
from lib.names import Names
from lib.state import State
from strategy.text import TextStrategy
import lib.cli
import lib.config

names = Names()


class StrategyNotFoundError(Exception):
    pass


def check_invalid_names(line, path, line_number):
    """Check the line and warn if it contains invalid names.
    @type  line: str
    @param line: Proze formatted line.
    @type  path: str
    @param path: Path to the proze file being parsed.
    @type  line_number: number
    @param line_number: Current line number in the file being parsed.
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
    elif args.doctype == 'text':
        return TextStrategy(options)
    raise StrategyNotFoundError(
        'Unrecognized strategy {}'.format(args.doctype)
    )


def execute_strategy(strategy, args, options):
    """Compile the proze project using the stragegy.
    @type  strategy: BaseStrategy
    @param strategy: Strategy to use.
    @type  args: object
    @param args: Parsed command line args.
    @type  options: DotMap
    @param options: Compile options parsed from the config file.
    """
    brackets = Brackets()
    comments = Comments()
    # TODO comments should be aware of brackets
    #   - don't recognize a comment if it's inside a bracket block
    state = State()
    output_path = args.output + '.' + args.doctype
    with strategy.compile(output_path) as compiler:
        for path in options.compile.order:
            with open(path, 'r') as proze_file:
                comments.reset()
                brackets.reset
                state.reset()
                line_number = 0
                for line in proze_file:
                    line_number = line_number + 1
                    line = comments.remove(line) # TODO make bracket aware
                    line = brackets.remove(line)
                    check_invalid_names(line, path, line_number)
                    if line:
                        compiler.write(line, state)
                    state.update(line) # TODO parsed or raw version of line?


def run():
    """Compile proze to target format."""
    args = lib.cli.parse()
    options = lib.config.load()
    if not options.compile.order:
        print('No proze files to compile.')
    else:
        strategy = determine_strategy(options)
        execute_strategy(strategy, args, options)


if __name__ == "__main__":
    run()

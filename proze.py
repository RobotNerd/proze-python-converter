#!/usr/bin/python3
from lib.comments import Comments
from lib.names import Names
from strategy.text import TextStrategy
import lib.cli
import lib.config

comments = Comments()
names = Names()


class StrategyNotFoundError(Exception):
    pass


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


def run():
    """Compile proze to target format."""
    args = lib.cli.parse()
    options = lib.config.load()
    strategy = determine_strategy(options)
    with strategy.compile(target_path) as compiler: #TODO output file name
        # TODO iterate through all *.proze files in config
        # TODO print message and exit if no files found to compile
        with open(path, 'r') as proze_file:
            comments.reset()
            line_number = 0
            for line in proze_file:
                line_number = line_number + 1
                line = comments.remove(line)
                check_invalid_names(line, path, line_number)
                if line:
                    comipler.write(line)


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


if __name__ == "__main__":
    run()

import argparse
import os


def parse():
    """Parse command line arguments.
    @rtype:  object
    @return: Parsed command line arguments.
    """
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description='Compile a proze project.')
    parser.add_argument(
        'doctype',
        choices=[
            'pdf',
            'txt',
        ],
        type=str,
        help='The output format of the compiled document.'
    )
    parser.add_argument(
        '--output',
        default='output',
        type=str,
        help='The name of the output file to generate.'
    )
    parser.add_argument(
        '--path',
        default=cwd,
        type=str,
        help='Path to the root folder of the proze project.'
    )
    return parser.parse_args()

#!/usr/bin/env python2.7
"""Change headers to an ISF-compatible format.

2012/09/05
Edward Liaw
"""
import sys
import argparse
import re

# Pattern to look for id number.
target = re.compile(r'>HcapG186R_SC(\d+)')
# Database name for species.
species = 'HcapG186AR'
# Abbreviation for the separation type.
abbr = 'SC'


def modify_headers(infile, species=species, abbr=abbr):
    """Change headers to ISF-compatible format.

    Args:
        infile: A filestream to read from.
    """
    for line in infile:
        if line.startswith('>'):
            try:
                number = int(target.match(line).group(1))
            except AttributeError:
                print >> sys.stderr, "Unmatched header:\n\t{}".format(line)
            else:
                line = ">{}_{}{:02d}\n".format(species, abbr, number)
        yield line


def parse_arguments():
    """Handle command-line arguments.

    Returns:
        args: Arguments passed in from the command-line."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     fromfile_prefix_chars='@')
    parser.add_argument('infile',
                        type=argparse.FileType('r'), nargs='?',
                        default=sys.stdin, help='input file')
    parser.add_argument('outfile',
                        type=argparse.FileType('w'), nargs='?',
                        default=sys.stdout, help='output file')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Handle I/O.
    with args.infile as infile, args.outfile as outfile:
        for line in modify_headers(infile):
            outfile.write(line)


if __name__ == "__main__":
    main()

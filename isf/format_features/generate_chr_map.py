#!/usr/bin/env python2.7
"""Generates a chromosome map for a fasta file.

2012/09/14
Edward Liaw
"""
import sys
import argparse
import re

re_chr_num = re.compile(r'Chr(?P<number>\d+)')


def parse_headers(infile):
    """Get fasta headers.

    Args:
        infile: A filestream to read from.
    """
    for line in infile:
        if line.startswith('>'):
            yield line.rstrip().lstrip('>')


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
        for i, header in enumerate(parse_headers(infile)):
            try:
                number = int(re_chr_num.search(header).group(1))
            except AttributeError:
                raise Exception("Not an expected header format: {}".format(header))
            output = (str(col) for col in (header, number, i + 1))
            print >> outfile, '\t'.join(output)


if __name__ == "__main__":
    main()

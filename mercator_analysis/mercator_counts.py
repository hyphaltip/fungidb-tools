#!/usr/bin/env python2.7
"""Generate simple statistical information from mercator output.

2012/09/24
Edward Liaw
"""
import sys
import argparse
import os
from collections import defaultdict

RAW = False

rootdir = "/eupath/data/apiSiteFiles/webServices/FungiDB/release-2.0/mercator"
# Mapping lengths
mapfile = 'alignments/map'
# Header file
genomefile = 'alignments/genomes'


def parse_size_from_agp(fh):
    """Parse out and sum the size of the genome from the agp file."""
    sum = 0
    for line in fh:
        spline = line.rstrip('\n').split('\t')
        sum += int(spline[2])
    return sum


def parse_size_from_map(fh):
    """Compute the total size of the syntenic regions from the map file."""
    sum_1 = sum_2 = 0
    for line in fh:
        spline = line.rstrip('\n').split('\t')
        start_1, end_1 = spline[2:4]
        start_2, end_2 = spline[6:8]
        sum_1 += abs(int(end_1) - int(start_1))
        sum_2 += abs(int(end_2) - int(start_2))
    return sum_1, sum_2


def parse_headers(fh):
    """Parse out species header from header file (genome)."""
    return fh.readline().rstrip('\n').split('\t', 1)


def parse_arguments():
    """Handle command-line arguments.

    Returns:
        args: Arguments passed in from the command-line."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     fromfile_prefix_chars='@')
    parser.add_argument('outfile',
                        type=argparse.FileType('w'), nargs='?',
                        default=sys.stdout, help='output file')
    parser.add_argument('-r', '--raw',
                        action='store_true', help='dump raw counts instead')
    return parser.parse_args()


def main():
    args = parse_arguments()

    global RAW
    RAW = args.raw

    genome_size = {}
    synteny_size = defaultdict(dict)

    for targetdir in os.listdir(rootdir):
        print >> sys.stderr, "Processing: {}".format(targetdir)
        targetdir = os.path.join(rootdir, targetdir)
        for fn in os.listdir(targetdir):
            species, ext = os.path.splitext(fn)
            if ext == '.agp':
                # Get the genome length.
                with open(os.path.join(targetdir, fn)) as infile:
                    genome_size[species] = parse_size_from_agp(infile)
        # Get the species order from the header file.
        with open(os.path.join(targetdir, genomefile)) as headerfh:
            species_1, species_2 = parse_headers(headerfh)
        # Get the syntenic region length.
        with open(os.path.join(targetdir, mapfile)) as mapfh:
            synteny_size_1, synteny_size_2 = parse_size_from_map(mapfh)
            synteny_size[species_1][species_2] = synteny_size_1
            synteny_size[species_2][species_1] = synteny_size_2

    ordered_species = sorted(synteny_size.keys())
    # Print the results.
    with args.outfile as outfile:
        print >> outfile, '\t' + '\t'.join(ordered_species)
        for species_1, counts in ((s, synteny_size[s]) for s in ordered_species):
            outlist = [species_1]
            for s in ordered_species:
                try:
                    if RAW:
                        outlist.append(format(counts[s], '.1e'))
                    else:
                        outlist.append(format(counts[s] / float(genome_size[species_1]), '.2%'))
                except KeyError:
                    outlist.append('')
            print >> outfile, '\t'.join(outlist)


if __name__ == "__main__":
    main()

#!/usr/bin/env python2.7
"""Download Genbank files in bulk.
Based on download_genbank.pl by Jason Stajich.

2012/09/05
Edward Liaw
"""
import sys
import argparse
import re
import os
import gzip
from os import path
from Bio import Entrez, SeqIO

# Matches the accession string format.
re_acc = re.compile(r'([A-Za-z_]+)(\d+)$')
# Format string for gzipped genbank files.
gzip_format = "{}.gbk.gz"


class InvalidAccessionException(Exception):
    """Raised when the accession code does not match the expected format."""
    pass


class EmptyQueryException(Exception):
    """Raised when an empty query set is passed (files already downloaded)."""
    pass


def parse_acc(acc_string):
    """Splits the numerical part of the NCBI accession code from the
    alphabetical.

    Args:
        acc_string: A valid NCBI accession code.

    Returns:
        A tuple of the alphabetical part and the numerical part.

    Raises:
        InvalidAccessionException if code does not match pattern.
    """
    try:
        letter, number = re_acc.match(acc_string).groups()
    except:
        raise InvalidAccessionException("Cannot parse {}".format(acc_string))
    else:
        return letter, number


def is_acc_in_basedir(avoid_acc, basedir, species):
    """Checks if accession code has a file in the path: basedir/species."""
    avoid_file = path.join(basedir, species, gzip_format.format(avoid_acc))
    return path.isfile(avoid_file)


def parse_target_file(infile, basedir, debug=False):
    """Parse out accession numbers to search for from tab separated file.

    Args:
        infile: Filestream of tab separated file
                (species name | accession codes separated by - or ,).

    Yields:
        Tuple of name and accession code generator.
    """

    for line in infile:
        if line.startswith(('#', '$')):
            # Commented out.
            continue

        species, accessions = line.rstrip().split('\t')

        def iter_query(accessions, basedir=basedir, species=species, quiet=False):
            """Generator to create query strings from accession codes.

            Args:
                accessions: String of comma-delimited accession code ranges.

            Yields:
                Tuple of (species | generator of tuples: (each accession query
                | list of queries to negate for files that already exist in the
                basedir)).

            Raises:
                EmptyQueryException if entire query set already has files in
                the basedir.
            """
            keep_query = 0
            for pair in accessions.split(','):
                try:
                    start, finish = pair.split('-', 2)
                except ValueError:
                    # Singular
                    try:
                        re_acc.match(accessions)
                    except InvalidAccessionException as e:
                        print >> sys.stderr, "Warning: {}".format(e)
                        continue

                    if not is_acc_in_basedir(accessions, basedir, species):
                        # Flag: Query is not empty.
                        keep_query += 1
                        yield accessions, ()
                else:
                    # Is a pair.
                    keep_range = 0
                    try:
                        s_letter, s_number = parse_acc(start)
                        f_letter, f_number = parse_acc(finish)
                        if f_letter != s_letter or int(s_number) > int(f_number):
                            # Invalid range.
                            raise InvalidAccessionException("Accession set does not match")

                        avoid = []
                        for i in xrange(int(s_number), int(f_number) + 1):
                            acc = "{}{:0{}d}".format(s_letter, i, len(s_number))
                            if is_acc_in_basedir(acc, basedir, species):
                                # If so, cancel them from the query.
                                avoid.append(acc)
                            else:
                                # Flag: Query is not empty.
                                keep_query += 1
                                keep_range += 1

                        # Check that files are not already downloaded.
                        if keep_range:
                            acc_range = "{}:{}".format(start, finish)
                            yield acc_range, avoid

                    except InvalidAccessionException as e:
                        print >> sys.stderr, "Warning: {} in pair {}".format(e, pair)
                        continue

            if not keep_query:
                # Final check to warn if queryset is empty.
                raise EmptyQueryException("Warning: {} already downloaded, skipping.".format(species))
            if not quiet:
                print >> sys.stderr, "Expected {} sequences for {}.".format(keep_query, species)

        yield species, iter_query(accessions)


def parse_arguments():
    """Handle command-line arguments.

    Returns:
        args: Arguments passed in from the command-line."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     fromfile_prefix_chars='@')
    parser.add_argument('infile',
                        type=argparse.FileType('r'), nargs='?',
                        default='../data_files/fungal_genbank_accessions.dat',
                        help="Tab-delimited file of genbank accession codes")
    parser.add_argument('-b', '--basedir',
                        default="../out", help="Directory to output data")
    parser.add_argument('-d', '--debug',
                        action='store_true', help="Debug mode")
    parser.add_argument('-q', '--quiet',
                        action='store_true', help="Quiet mode")
    parser.add_argument('-s', '--batch_size',
                        type=int, default=2, help="Download batch size")
    return parser.parse_args()


def main():
    args = parse_arguments()
    basedir = args.basedir
    debug = args.debug
    quiet = args.quiet
    batch_size = args.batch_size

    # Set email for NCBI.
    Entrez.email = "ed.liaw@fungidb.org"

    # Read target file.
    with args.infile as infile:
        for species, accessions in parse_target_file(infile, basedir, quiet):
            keep = []
            avoid = []
            targetdir = path.join(basedir, species)
            downloaded = 0

            try:
                for keep_acc, avoid_accs in accessions:
                    keep.append(keep_acc)
                    for acc in avoid_accs:
                        avoid.append(acc)
            except EmptyQueryException as e:
                # Query set already downloaded.
                print >> sys.stderr, e
                continue
            # Insert OR's between wanted queries and NOT's in front of negated
            # queries.
            term = ' '.join((' OR '.join(keep), ' '.join('NOT {}'.format(acc) for acc in avoid)))
            if debug:
                print "Query: {}".format(term)

            # Build directory
            try:
                os.makedirs(targetdir)
            except OSError:
                # Ignore if folder already exists.
                pass

            # Search for query in NCBI nucleotide.
            search_handle = Entrez.esearch(db='nucleotide', term=term,
                                           field='ACCN', usehistory='y')
            search_results = Entrez.read(search_handle)
            search_handle.close()

            # Store search results.
            webenv = search_results['WebEnv']
            query_key = search_results['QueryKey']
            count = int(search_results['Count'])
            if not quiet:
                print "Retrieved {} sequences for {}.".format(count, species)

            # Download the search results.
            for start in xrange(0, count, batch_size):
                fetch_handle = Entrez.efetch(db='nucleotide',
                                             rettype='gbwithparts',
                                             retmode='text', retstart=start,
                                             retmax=batch_size, webenv=webenv,
                                             query_key=query_key)
                records = SeqIO.parse(fetch_handle, 'gb')
                for record in records:
                    acc = record.name
                    fn = path.join(targetdir, gzip_format.format(acc))
                    if debug:
                        print "Downloading {}..".format(fn)
                    with gzip.open(fn, 'wb') as outfile:
                        SeqIO.write(record, outfile, 'gb')
                        downloaded += 1
                    if not quiet:
                        print "{} complete.".format(acc)
                fetch_handle.close()
            if not quiet:
                print "Downloaded {} of {} sequences.".format(downloaded, count)


if __name__ == "__main__":
    main()

#!/usr/bin/env python2.7
"""Add gene and exon features to a GFF3 file that only has mRNA and CDS
features.

2012/09/20
Edward Liaw
"""
import sys
import argparse
from collections import MutableMapping, MutableSequence, defaultdict
from copy import deepcopy

DEBUG = False
GFF_COLUMNS = ('seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase')
GFF_ATTRIBUTES = ('ID', 'Parent')
MRNA_FORMAT = 'mRNA_{}'
CDS_FORMAT = 'cds{:02d}_{}'
EXON_FORMAT = 'exon{:02d}_{}'


class UnknownTypeException(Exception):
    pass


class WrongGroupException(Exception):
    pass


class Gff(MutableMapping):
    """Encapsulate a GFF row as an object.

    Attributes:
        _properties: Dictionary of columns 1-8.  Mapping-style access on the
                     instance, i.e. gff_row['type'].
        attributes: Dictionary of attributes in column 9.
        index: Indicates position in original file.
    """
    def __init__(self, properties, attributes, index):
        self._properties = properties
        self.attributes = attributes
        self.index = index

    @classmethod
    def from_string(cls, row, index=0):
        """Initialize from a string: a row read from a GFF file."""
        sprow = row.rstrip().split('\t')
        attr_row = sprow.pop().rstrip(';')
        # Set the properties (cols 1-8).
        properties = {k: v for k, v in zip(GFF_COLUMNS, sprow)}
        # Set the attributes (col 9).
        attributes = {}
        for attr in attr_row.split(';'):
            key, val = attr.split(' ', 1)
            attributes[key] = val.strip('"')
        return cls(properties, attributes, index)

    def __getitem__(self, key):
        """Properties accessible by mapping syntax."""
        return self._properties[key]

    def __setitem__(self, key, value):
        self._properties[key] = value

    def __delitem__(self, key):
        del self._properties[key]

    def __iter__(self):
        return iter(self._properties)

    def __len__(self):
        return len(self._properties)

    def __lt__(self, other):
        """Sortable by index."""
        return self.index < other.index

    def __copy__(self):
        return Gff(self._properties.copy(), self.attributes.copy(), self.index)

    def __str__(self):
        """Write me back as a string."""
        properties = [self[col] for col in GFF_COLUMNS]
        attributes = []
        for attr in GFF_ATTRIBUTES:
            try:
                attributes.append('{} "{}"'.format(attr, self.attributes[attr]))
            except KeyError:
                pass
        # Add the attributes as the final column.
        properties.append(';'.join(attributes) + ';')
        return '\t'.join(properties)

    def is_subset(self, other):
        """Check if we are contained in another feature."""
        my_id = self['seqid']
        your_id = other['seqid']
        my_s = self['start']
        my_e = self['end']
        your_s = other['start']
        your_e = other['end']
        return my_id == your_id and my_s >= your_s and my_e <= your_e

    def is_intersecting(self, other):
        """Check if we intersect with another feature."""
        my_id = self['seqid']
        your_id = other['seqid']
        my_s = int(self['start'])
        my_e = int(self['end'])
        your_s = int(other['start'])
        your_e = int(other['end'])
        return my_id == your_id and ((your_s <= my_s <= your_e) or (your_s <= my_e <= your_e))

    def is_child(self, other):
        """Check lineage with another feature."""
        my_parent = self.attributes['Parent']
        your_id = other.attributes['ID']
        return my_parent == your_id


class GffHierarchy(MutableSequence):
    """Data structure to store a gene and its child features.

    Attributes:
        gene: The gene feature at the root of this hierarchy.
        counts: Counter of how many of each type is in _features.
        _features: List of child features.
    """
    def __init__(self, gene, features):
        self.gene = gene
        self.counts = defaultdict(int)
        self._features = features

    @classmethod
    def from_gene(cls, gene):
        return cls(gene, [])

    def __getitem__(self, index):
        """Features accessible by list index."""
        return self._features[index]

    def __setitem__(self, index, value):
        self._features[index] = value

    def __delitem__(self, index):
        del self._features[index]

    def __iter__(self):
        return iter(self._features)

    def __len__(self):
        return len(self._features)

    def insert(self, index, value):
        self.counts[value['type']] += 1
        self._features.insert(index, value)

    def flatten(self):
        """Return a list of all the features, including the root gene feature."""
        return [self.gene] + self._features


def sort_stored(stored):
    """Reorder the stored rows as in the original file."""
    flat = []
    for group in stored:
        if DEBUG and len(group) < 1:
            # Group only has gene in it.
            print >> sys.stderr, "Possible pseudogene:\n{}".format(group.gene)
        flat += group.flatten()
    for output_row in sorted(flat):
        yield output_row


def mRNAid_to_geneid(m_id):
    """Reduce the id to its accession code."""
    return m_id.lstrip('mRNA:')


def gene_from_mRNA(mRNA):
    """Create a gene out of an mRNA feature."""
    gene = deepcopy(mRNA)
    gene['type'] = 'gene'
    mRNA.attributes['ID'] = MRNA_FORMAT.format(gene.attributes['ID'])
    mRNA.attributes['Parent'] = gene.attributes['ID']
    return gene, mRNA


def exon_from_cds(cds, counts):
    """Create an exon out of a CDS feature."""
    exon = deepcopy(cds)
    exon['type'] = 'exon'
    exon.attributes['ID'] = EXON_FORMAT.format(counts['exon'] + 1, exon.attributes['ID'])
    cds.attributes['ID'] = CDS_FORMAT.format(counts['CDS'] + 1, cds.attributes['ID'])
    return exon, cds


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
    parser.add_argument('-d', '--debug',
                        action='store_true')
    return parser.parse_args()


def main():
    args = parse_arguments()

    global DEBUG
    DEBUG = args.debug
    if DEBUG:
        print >> sys.stderr, "Debug on"

    # Handle I/O.
    with args.infile as infile, args.outfile as outfile:
        stored = []
        index = 0
        current_group = None
        for line in infile:
            if line.lstrip().startswith('#'):
                # Skip comments.
                print >> outfile, line
                continue
            row = Gff.from_string(line.rstrip(), index)
            index += 1
            type = row['type']

            if 'Parent' not in row.attributes:
                # A parent row.
                # Check for overlap / print if safe.
                for group in stored:
                    if row.is_intersecting(group.gene):
                        # Overlapping.
                        if DEBUG:
                            print >> sys.stderr, "Overlapping genes:\n{}\n{}".format(row, group.gene)
                        break
                else:
                    # No overlap with stored groups: safe to print.
                    for output_row in sort_stored(stored):
                        print >> outfile, output_row
                    # Reset stored values.
                    stored = []
                    index = 0
                    row.index = index
                    index += 1

                # Check type.
                if type == 'gene':
                    # New group.
                    current_group = GffHierarchy.from_gene(row)
                elif type == 'mRNA':
                    # Create an equivalent gene.
                    row.attributes['ID'] = mRNAid_to_geneid(row.attributes['ID'])
                    gene, mRNA = gene_from_mRNA(row)
                    mRNA.index = index
                    index += 1
                    # New group.
                    current_group = GffHierarchy.from_gene(gene)
                    current_group.append(mRNA)
                else:
                    # Not a type I expect to be parent-less.
                    raise UnknownTypeException("Unexpected type: {}".format(row['type']))
                stored.append(current_group)
            else:
                # A child row.
                if type == 'CDS':
                    g_id = mRNAid_to_geneid(row.attributes['Parent'])
                    row.attributes['Parent'] = g_id
                    for group in stored:
                        # Find my parent.
                        if row.is_child(group.gene):
                            current_group = group
                            break
                    else:
                        # Did not find a parent.
                        raise WrongGroupException("Row's parent does not match nearby groups:\n{}".format(row))
                    row.attributes['ID'] = g_id
                    row.attributes['Parent'] = MRNA_FORMAT.format(g_id)
                    exon, cds = exon_from_cds(row, current_group.counts)
                    cds.index = index
                    index += 1
                    current_group.append(exon)
                    current_group.append(cds)
                else:
                    # Haven't accounted for this type yet.
                    raise UnknownTypeException("Unexpected type: {}".format(row['type']))
                    current_group.append(row)
        # Final dump of stored rows.
        for output_row in sort_stored(stored):
            print >> outfile, output_row


if __name__ == "__main__":
    main()

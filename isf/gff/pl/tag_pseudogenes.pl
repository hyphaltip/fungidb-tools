#!/usr/bin/env perl
# Relabel pseudogenes in a eupathdb gff file.
# 2012-09-14
# Edward Liaw
use strict;
use warnings;

use Getopt::Long;
Getopt::Long::Configure(qw(bundling));

# Handle arguments.
my $debug = '';
&GetOptions('d|debug' => \$debug);
$#ARGV >= 0 or die "Need an input file";
my $infile = shift;

# Ordered properties and attributes.
my @gff_columns = qw(seqid source type start end score strand phase);
my @gff_attributes = qw(ID Parent);

sub parse_gff {
	# Parse a gff row into a data structure: hash of properties and hash of attributes.
	# Args:
	# 	line: string of a row in the gff file.
	# Returns:
	# 	gff row: [\%properties, \%attributes]
	
	my $line = shift;
	my @spline = split(/\t/, $line);
	my $attr_row = pop(@spline);

	# Get the feature information for this row.
	my %properties = ();
	@properties{@gff_columns} = @spline;

	my %attributes = ();
	foreach (split(/;/, $attr_row)) {
		my ($key, $val) = split(/ /, $_);
		$attributes{$key} = $val;
	}
	return [\%properties, \%attributes];
}

sub row_to_s {
	# Formats a gff data structure to a string.
	# Args:
	# 	gff_row: [\%properties, \%attributes]
	# Returns:
	# 	string representation of the row

	my $gff_row = shift;
	my ($p, $a) = @$gff_row;
	my %properties = %$p;
	my %attributes = %$a;

	# Ordered set of properties (by list of gff columns)
	my @p_ordered = map { $properties{$_} } @gff_columns;
	# Ordered set of attributes (by list of gff attributes)
	my @a_ordered = map { "$_ $attributes{$_}" } grep { exists($attributes{$_}) } @gff_attributes;
	my $attr_col = join(';', @a_ordered) . ';';
	push(@p_ordered, $attr_col);

	my $output = join("\t", @p_ordered);
	return $output . "\n";
}

sub print_stored {
	# Prints out gff rows, labeling pseudogenes in the process.
	# Args:
	# 	stored: array of [\%properties, \%attributes]

	my $s = shift;
	my @stored = @$s;
	# Pull out all the types in this group of rows.
	my @types = map { $_->[0]->{type} } @stored;
	if (not grep { $_ eq 'CDS' } @types) {
		# No CDS: mark the row.
		foreach my $gff_row (@stored) {
			my ($p, $a) = @$gff_row;
			my %properties = %$p;
			if ($properties{type} eq 'gene') {
				# Change genes to pseudogenes.
				$properties{type} = 'pseudogene';
				print STDERR &row_to_s([\%properties, $a]) if ($debug);
			}
			print &row_to_s([\%properties, $a]);
		}
	}
	else {
		# There is a CDS: print normally.
		foreach my $gff_row (@stored) {
			print &row_to_s($gff_row);
		}
	}
}

print STDERR "Debug on\n" if ($debug);

my @stored = ();
open INFILE, '<', $infile or die "Can't open $infile for reading!";
while (my $line = <INFILE>) {
	chomp($line);
	# Skip comments (lines that start with a #).
	next if ($line =~ /^\s*#/);
	my ($properties, $attributes) = @{&parse_gff($line)};

	if (exists($attributes->{Parent})) {
		# Child feature.
		push(@stored, [$properties, $attributes]);
		next;
	}
	else {
		# Parent feature.
		&print_stored(\@stored);
		# Empty stored list.
		@stored = ([$properties, $attributes]);
	}
}
close INFILE;
&print_stored(\@stored);

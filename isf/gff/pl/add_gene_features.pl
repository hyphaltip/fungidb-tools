#!/usr/bin/env perl
# Add gene and exon features to a gff file, preserving parent-child relationships.
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
my $mRNA_format = "mRNA_%s";
my $exon_format = "exon%02d_%s";
my $cds_format = "cds%02d_%s";

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
		$val =~ s/^"(.*)"$/$1/;
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
	my @a_ordered = map { "$_ \"$attributes{$_}\"" } grep { exists($attributes{$_}) } @gff_attributes;
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

sub new_gene_feature {
	# Create a gene feature corresponding to the given mRNA feature.
	# Args:
	# 	mRNA_row: a gff row with type mRNA
	# Returns:
	# 	gene_row: a corresponding gene row
	#	mRNA_row: a modified child mRNA row

	my $gff_row = shift;
	my ($p, $a) = @$gff_row;
	my %gene_properties = %$p;
	my %gene_attributes = %$a;

	my %mRNA_attributes = %$a;

	$gene_properties{type} = 'gene';
	$mRNA_attributes{ID} = sprintf($mRNA_format, $mRNA_attributes{ID});
	$mRNA_attributes{Parent} = $gene_attributes{ID};

	return [[\%gene_properties, \%gene_attributes], [$p, \%mRNA_attributes]];
}

sub new_exon_feature {
	# Create a exon feature corresponding to the given CDS feature.
	# Args:
	# 	cds_row: a gff row with type CDS
	# Returns:
	# 	exon_row: a corresponding exon row
	#	cds_row: a modified cds row

	my $gff_row = shift;
	my $count = shift;
	my ($p, $a) = @$gff_row;
	my %exon_properties = %$p;
	my %exon_attributes = %$a;

	my %cds_attributes = %$a;

	$exon_properties{type} = 'exon';
	$exon_attributes{ID} = sprintf($exon_format, $count, $exon_attributes{ID});
	$cds_attributes{ID} .= sprintf($cds_format, $count, $cds_attributes{ID});

	return [[\%exon_properties, \%exon_attributes], [$p, \%cds_attributes]];
}

print STDERR "Debug on\n" if ($debug);

my $gene_count = 0;
my $cds_count = 0;
my $last_gid;
open INFILE, '<', $infile or die "Can't open $infile for reading!";
while (my $line = <INFILE>) {
	chomp($line);
	# Skip comments (lines that start with a #).
	if ($line =~ /^\s*#/) {
		print $line . "\n";
		next;
	}
	my ($properties, $attributes) = @{&parse_gff($line)};
	my $type = $properties->{type};

	if ($type eq 'mRNA') {
		# mRNA found.
		if ($attributes->{ID} =~ /mRNA:(\S+)/) {
			$last_gid = $1;
			$attributes->{ID} = $last_gid;
		}
		else {
			warn "Non-matching ID: " . $attributes->{ID};
		}
		# Add a gene feature.
		my ($gene, $mRNA) = @{&new_gene_feature([$properties, $attributes])};
		print &row_to_s($gene);
		print &row_to_s($mRNA);
		$gene_count++;
		$cds_count = 0;
	}
	elsif ($type eq 'CDS') {
		$cds_count++;
		# Fix attributes.
		$attributes->{ID} = $last_gid;
		$attributes->{Parent} = sprintf($mRNA_format, $last_gid);
		my ($exon, $cds) = @{&new_exon_feature([$properties, $attributes], $cds_count)};
		print &row_to_s($exon);
		print &row_to_s($cds);
	}
	else {
		warn "Type other than mRNA or CDS found: $type";
		print &row_to_s([$properties, $attributes]);
	}
}
close INFILE;
print STDERR "Added $gene_count genes.\n" if $debug;

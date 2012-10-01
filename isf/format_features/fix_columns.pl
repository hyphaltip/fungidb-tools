#!/usr/bin/env perl
# Modify first 2 columns of a gtf file.
# 2012-08-29
# Edward Liaw
use strict;
use warnings;

use Getopt::Long;
Getopt::Long::Configure(qw(bundling));

# Command line args.
my $id = '';
my $source = '';
my $regex = 'chr';	# The string preceding the number in the chromosome.
&GetOptions('i|id=s' => \$id,
	    's|source=s' => \$source,
            'r|regex:s' => \$regex);
$#ARGV == 0 or die "Too few arguments";
my $infile = shift;

# Command line args.
open INFILE, '<', $infile or die "Can't open $infile for reading!";

while (my $line = <INFILE>) {
	my @spline = split(/\t/, $line);
	# Get the contig number.
	$spline[0] =~ m/>$regex(\d+)/;
	my $chr = $1;
	# Rewrite columns.
	$spline[0] = sprintf("%s\_SC%02d", $id, $chr);
	$spline[1] = $source;
	print join("\t", @spline);
}
close INFILE;

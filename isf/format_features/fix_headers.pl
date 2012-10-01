#!/usr/bin/env perl
# Set custom header for fasta file.
# 2012-08-29
# Edward Liaw
use strict;
use warnings;

use Getopt::Long;
Getopt::Long::Configure(qw(bundling));

# Command line args.
my $id = '';
my $regex = 'chr';	# The string preceding the number in the chromosome.
&GetOptions('i|id=s' => \$id,
	    'r|regex:s' => \$regex);
$#ARGV == 0 or die "Too few arguments";
my $infile = shift;

open INFILE, '<', $infile or die "Can't open $ARGV[0] for reading!";

while (my $line = <INFILE>) {
	if ($line =~ m/^>/i) {
		# Is a header.
		# Get the contig number.
		$line =~ m/>$regex(\d+)/;
		my $count = $1;
		$line = sprintf ">%s\_Chr%02d\n", $id, $count;
	}
	print $line
}

close INFILE;

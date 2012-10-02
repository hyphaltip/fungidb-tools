#!/usr/bin/env perl
# Extract genes and product names from genome summary file.
# 2012-09-10
# Edward Liaw
use strict;
use warnings;

# Command line args.
$#ARGV == 0 or die "Too few arguments";
open INFILE, '<', $ARGV[0] or die "Can't open $ARGV[0] for reading!";

# Find the columns we want to save.
chomp(my $header = <INFILE>);
my @headings = split(/\t/, $header);
my $tab = 0;
my $locus_index = 0;
my $name_index = 0;
foreach my $heading (@headings) {
	if ($heading eq "LOCUS") {
		$locus_index = $tab;
	}
	elsif ($heading eq "NAME") {
		$name_index = $tab;
	}
	$tab++;
}

while (my $line = <INFILE>) {
	chomp $line;
	my @spline = split(/\t/, $line);
	print "$spline[$locus_index]\t$spline[$name_index]\n";
}

close INFILE;

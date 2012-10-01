#!/usr/bin/perl

use strict;
#use lib "$ENV{GUS_HOME}/lib/perl";

use DBI;
use Data::Dumper;
use XML::Simple;
use XML::Writer;
use IO;
use URI::Escape;


if (!@ARGV) {
print ("Usage:  makeAttributions.pl\tinputFile\n\nInput File structure:\nData Source Name\tDisplay Name\n\nExample\npfal3D7_genome_mitochondrial_RSRC\t Mitochondrial and Plastid Genomes\n\n");
}


my $writer = new XML::Writer( OUTPUT => "STDOUT" ,DATA_MODE => 'true', DATA_INDENT => 3);

$writer->xmlDecl( 'UTF-8' );
$writer->startTag( 'dataSourceAttributions');

open (fileHandle, shift);

while (<fileHandle>) {
  chomp;
  my $dsName = $_;
  my @names = split(/\t/,$dsName);
  $names[0] =~ s/ //g; 

  $writer->startTag( 'dataSourceAttribution', 'resource' => $names[0], 'overriddingType' =>'', 'overridingSubtype' => '', 'ignore' =>'');
  print ("\n");
  $writer->startTag( 'displayCategory'); $writer->endTag( 'displayCategory');
  print ( "\n"); 
  $writer->startTag( 'publications');
  $writer->endTag( 'publications');
  print ( "\n");


  $writer->startTag( 'contacts');
  $writer->startTag( 'contact', 'isPrimaryContact' => 'true' );
  $writer->startTag( 'name' );$writer->endTag( 'name');
  $writer->startTag( 'email' );$writer->endTag( 'email');
  $writer->startTag( 'institution' );$writer->endTag( 'institution');
  $writer->startTag( 'address' );$writer->characters( "" );$writer->endTag( 'address');
  $writer->startTag( 'city' );$writer->characters( "" );$writer->endTag( 'city');
  $writer->startTag( 'state' );$writer->characters( "" );$writer->endTag( 'state');
  $writer->startTag( 'country' );$writer->characters( "" );$writer->endTag( 'country');
  $writer->startTag( 'zip' );$writer->characters( "" );$writer->endTag( 'zip');
  $writer->endTag( 'contact' );
  $writer->endTag( 'contacts');
  print ( "\n");

  $writer->startTag( 'displayName'); print("\<![CDATA[$names[1]]]\>" ); $writer->endTag( 'displayName');
  print ( "\n");
  $writer->startTag( 'summary'); print( "\<![CDATA[]]\>" ); $writer->endTag( 'summary');
  print ( "\n");
  $writer->startTag( 'protocol') ; $writer->endTag( 'protocol');
  $writer->startTag( 'caveat'); $writer->endTag( 'caveat');
  $writer->startTag( 'acknowledgement'); $writer->endTag( 'acknowledgement');
  $writer->startTag( 'releasePolicy'); $writer->endTag( 'releasePolicy');
  print ( "\n");
  $writer->startTag( 'description'); print( "\<![CDATA[]]\>" ); $writer->endTag( 'description');
  print ( "\n");


  $writer->startTag( 'links' );
  $writer->startTag( 'link' );
  $writer->startTag( 'type' ); $writer->characters( "publicUrl" ); $writer->endTag( 'type');
  $writer->startTag( 'url' ); $writer->endTag( 'url');
  $writer->startTag( 'linkDescription' ); $writer->characters( "" ); $writer->endTag( 'linkDescription');
  $writer->endTag( 'link' );
  $writer->endTag( 'links' );
  print ( "\n");

  $writer->emptyTag( 'wdkReference', 'recordClass' => '', 'type' => '', 'name' => '');
  print ( "\n");
  $writer->endTag( 'dataSourceAttribution');
}

$writer->endTag( 'dataSourceAttributions');



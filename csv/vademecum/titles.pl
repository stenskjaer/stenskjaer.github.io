#!/usr/bin/env perl -w
use strict;
use warnings;

# Open cwd, load all files starting with grep into array, close dir
opendir(DIR, '.') or die "Cannot open dir";
my @files = grep { /^Lektion.*?$/ } readdir(DIR);
closedir(DIR);

my $i = 1;						# first number
foreach my $file (@files) {
	# open the old and new files
	open my $in,  '<',  $file      or die "Can't read old file: $!";
	open my $out, '>', sprintf("lektion%02d.csv", $i) or die "Can't write new file: $!";
	
	# print filename to new file
	print $out substr($file, 0, -4) . "\n";
	
	# print remaining lines of old file to new file
	while ( <$in> ) {
		print $out $_;
	}
	
	$i++;						# increment for file-nameing
	
	close $out;					# close new and
	unlink $file;				# delete old file
}



#!/usr/bin/perl
# manage.pl

# TODO: rather one single script, and one CMakeLists, at top level

use lib '../manage';
use Build;
use Execute;
use Platform;
use Pyenv;
use Test;

use Getopt::Long;
use POSIX;
use Cwd;

my $usage = "usage: $0 [-h]
     -h: help\n";

my $helpDoc = "Prepare environment, build everything and run tests.
     -h | --help: this help

     -q | --quiet: only output errors
     -v | --verbose: output everything
     --build-verbose: build in verbose mode

     -c | --clean: clean pyenv and build directory
     -p | --prepare: create pyenv, run Conan and CMake
     -m | --cmake: run CMake

     --release: build in release mode
     --debug: build in debug mode
";

Getopt::Long::Configure("bundling");
GetOptions(
           "help|h" => \$help,
           "quiet|q" => \$quiet,
           "verbose|v" => \$verbose,
           "build-verbose" => \$buildVerbose,
           "clean|c" => \$clean,
           "prepare|p" => \$prepare,
           "cmake|m" => \$cmake,
           "release" => \$release,
           "debug" => \$debug
          ) or die $usage;
if ($help) {
    print "$usage\n";
    print "$helpDoc\n";
    exit 0;
}
my $sum = scalar grep {defined($_)} $clean, $prepare, $cmake, $release, $debug;
my $all = ($sum == 0) ? 1 : 0;
if ($all) {
    $prepare = 1;
    $release = 1;
    $debug = 1;
}

if ($buildVerbose) {
    $ninja .= " -v";
}
my $currentDirectory = getcwd;
configurePyenvUsage($currentDirectory, $verbose);
my $pythonRequirementsFile = "$currentDirectory/../requirements.txt";


if ($clean) {
    cleanMiscArtefacts($verbose);
    cleanBuild($verbose);
    cleanPyenv($verbose);
}

if ($prepare) {
    preparePyenv($pythonRequirementsFile, $verbose);
    conanInstall($verbose);
    runCMake($currentDirectory, $verbose);
}

if ($cmake) {
    runCMake($currentDirectory, $verbose);
}

if ($release) {
    build("Release", $verbose);
    runTest("Release", $verbose);
}

if ($debug) {
    build("Debug", $verbose);
    runTest("Debug", $verbose);
}

print "${okColour}Done${normalText}\n" if (! $quiet);
exit 0;

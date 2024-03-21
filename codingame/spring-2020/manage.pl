#!/usr/bin/perl
# manage.pl

use lib '../../manage';
use Build;
use Execute;
use Platform;
use Pyenv;
use PythonStatic;
use Test;

use Cwd;
use File::Basename;
use Getopt::Long;

my $usage = "usage: $0 [-h]
     -h: help\n";

my $helpDoc = "Prepare environment, build everything and run tests.

     -h | --help: this help

     -q | --quiet: only output errors
     -v | --verbose: output everything

     -c | --clean: clean pyenv
     -p | --prepare: create pyenv

     --check: run Python code static analysis
     --test: run tests
     --tests: optional tests names to run the unit tests
";

Getopt::Long::Configure("bundling");
GetOptions(
           "help|h" => \$help,
           "quiet|q" => \$quiet,
           "verbose|v" => \$verbose,
           "clean|c" => \$clean,
           "prepare|p" => \$prepare,
           "check" => \$check,
           "test" => \$test,
           "tests=s" => \$tests
          ) or die $usage;
if ($help) {
    print "$usage\n";
    print "$helpDoc\n";
    exit 0;
}
my $sum = scalar grep {defined($_)} $clean, $prepare, $check, $test;
my $all = ($sum == 0) ? 1 : 0;
if ($all) {
    $check = 1;
    $test = 1;
}

my $rootDirectory = dirname(Cwd::abs_path($0));
configurePyenvUsage($rootDirectory, $verbose);
my $pythonRequirementsFile = "$rootDirectory/requirements.txt";
my $mypyConfigFile = "../../.mypyrc";
my $pycodestyleConfigFile = "../../.pycodestyle";
my $pylintRcFile = "../../.pylintrc";
my $pylintReferenceFile = "pylint_reference.txt";
my $pythonFiles = "*.py";

if ($clean) {
    cleanMiscArtefacts($verbose);
    cleanPyenv($verbose);
}
if ($prepare) {
    preparePyenv($pythonRequirementsFile, $verbose);
}
if ($check) {
    runPythonCheck($mypyConfigFile, $pycodestyleConfigFile, $pylintRcFile, $pylintReferenceFile, $pythonFiles, $verbose);
}
if ($test) {
   if ($tests) {
        executeTestCommand("$pyenv; $pytest -vs $tests", "run specific tests", $verbose);
    } else {
        executeTestCommand("$pyenv; $pytest -vs $pythonFiles", "run tests", $verbose);
    }
}

print "${okColour}Done${normalText}\n" if (! $quiet);
exit 0;

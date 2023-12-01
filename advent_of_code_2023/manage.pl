#!/usr/bin/perl
# manage.pl

use lib '../manage';
use Build;
use CppStatic;
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
This script must be run from a sub-directory, such as skeleton for example:
challenges/skeleton > ../manage.pl -v

     -h | --help: this help

     -q | --quiet: only output errors
     -v | --verbose: output everything

     -c | --clean: clean pyenv and build directory
     -p | --prepare: create pyenv, run Conan and CMake
     -m | --cmake: run CMake

     --python-check: run mypy, pycodestyle and pylint on Python code
     --test: run tests
     --tests: optional unit tests names
";

Getopt::Long::Configure("bundling");
GetOptions(
           "help|h" => \$help,
           "quiet|q" => \$quiet,
           "verbose|v" => \$verbose,
           "clean|c" => \$clean,
           "prepare|p" => \$prepare,
           "python-check" => \$pythonCheck,
           "test" => \$test,
           "tests=s" => \$tests
          ) or die $usage;
if ($help) {
    print "$usage\n";
    print "$helpDoc\n";
    exit 0;
}
my $sum = scalar grep {defined($_)} $clean, $prepare, $pythonCheck, $test;
my $all = ($sum == 0) ? 1 : 0;
if ($all) {
    $prepare = 1;
    $test = 1;
    if (platformIsLinux()) {
        $pythonCheck = 1;
    }
}

my $rootDirectory = dirname(Cwd::abs_path($0));
#my $currentDirectory = getcwd;
configurePyenvUsage($rootDirectory, $verbose);
my $mypyConfigFile = ".mypyrc";
my $pycodestyleConfigFile = "../.pycodestyle";
my $pylintRcFile = "../.pylintrc";
my $pylintReferenceFile = "pylint_reference.txt";
my $pythonFiles = "src";
my $pythonRequirementsFile = "requirements.txt";

if ($clean) {
    cleanMiscArtefacts($verbose);
    cleanPyenv($verbose);
}
if ($prepare) {
    preparePyenv($pythonRequirementsFile, $verbose);
}
if ($pythonCheck) {
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

#!/usr/bin/perl
# manage.pl

use lib '../manage';
use Configure;
use Execute;
use Platform;
use Prepare;
use Run;

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
     -p | --prepare: create build directory, pyenv, and call cmake

     --build-release: build the libraries, in release mode
     --build-debug: build the libraries, in debug mode
     --release: build command line tools, in release mode
     --debug: build command line tools, in debug mode
";

Getopt::Long::Configure("bundling");
GetOptions(
           "help|h" => \$help,
           "quiet|q" => \$quiet,
           "verbose|v" => \$verbose,
           "build-verbose" => \$buildVerbose,
           "clean|c" => \$clean,
           "prepare|p" => \$prepare,
           "build-release" => \$buildRelease,
           "build-debug" => \$buildDebug,
           "release" => \$release,
           "debug" => \$debug
          ) or die $usage;
if ($help) {
    print "$usage\n";
    print "$helpDoc\n";
    exit 0;
}

my $sum = scalar grep {defined($_)} $clean, $prepare, $buildRelease, $buildDebug,
    $release, $debug;
my $all = ($sum == 0) ? 1 : 0;
if ($all) {
    $prepare = 1;
    $buildRelease = 1;
    $buildDebug = 1;
    $release = 1;
    $debug = 1;
}
$buildRelease = ($buildRelease || $release);
$buildDebug = ($buildDebug || $debug);

if ($buildVerbose) {
    $ninja .= " -v";
}

my $currentDirectory = getcwd;

configurePyenvUsage($currentDirectory, $verbose);
my $pythonRequirementsFile = "$currentDirectory/../requirements.txt";

if ($clean) {
    runClean();
}
if ($prepare) {
    runPrepare();
}
if ($buildRelease) {
    runBuildRelease();
}
if ($release) {
    runRelease();
}
if ($buildDebug) {
    runBuildDebug();
}
if ($debug) {
    runDebug();
}

print "${okColour}Done${normalText}\n" if (! $quiet);
exit 0;


sub runClean {
    if (platformIsLinux()) {
        foreach $link ("main", "main_debug") {
            executeCommandIgnoreReturnCode("$rm $link", "clean Linux binary link", $verbose);
        }
    }
    cleanMiscArtefacts($verbose);
    cleanBuild($verbose);
    cleanPyenv($verbose);
}

sub runPrepare {
    preparePyenv($pythonRequirementsFile, $verbose);
    prepareBuild($currentDirectory, $verbose);
}

sub runBuildRelease {
    executeTestCommand("$pyenv; cd $releaseBuildDirectory; $ninja", "build in Release mode", $verbose);
}

sub runBuildDebug {
    executeTestCommand("$pyenv; cd $debugBuildDirectory; $ninja", "build in Debug mode", $verbose);
}

sub runRelease {
    if (platformIsLinux()) {
        executeTestCommand("ln -sf $releaseBuildDirectory/main main",
            "create link to main binary in Release mode", $verbose);
    }
}

sub runDebug {
    if (platformIsLinux()) {
        executeTestCommand("ln -sf $debugBuildDirectory/main main_debug",
            "create link to main binary in Debug mode", $verbose);
    }
}

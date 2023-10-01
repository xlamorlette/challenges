#!/usr/bin/perl
# manage.pl

# TODO: rather one single script, and one CMakeLists, at top level

use lib '../manage';
use Build;
use Execute;
use Platform;
use Pyenv;

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
           "release" => \$release,
           "debug" => \$debug
          ) or die $usage;
if ($help) {
    print "$usage\n";
    print "$helpDoc\n";
    exit 0;
}

my $sum = scalar grep {defined($_)} $clean, $prepare, $release, $debug;
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
    runClean();
}
if ($prepare) {
    runPrepare();
}
if ($release) {
    runBuildRelease();
    runTest("Release");
}
if ($debug) {
    runBuildDebug();
    runTest("Debug");
}

print "${okColour}Done${normalText}\n" if (! $quiet);
exit 0;


sub runClean {
    if (platformIsLinux()) {
        foreach $link ("command_line_release", "command_line_debug") {
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
    build("Release", $verbose);
    if (platformIsLinux()) {
        executeTestCommand("ln -sf $releaseBuildDirectory/command_line/command_line command_line_release",
            "create link to command_line binary in Release mode", $verbose);
    }
}

sub runBuildDebug {
    build("Debug", $verbose);
    if (platformIsLinux()) {
        executeTestCommand("ln -sf $debugBuildDirectory/command_line/command_line command_line_debug",
            "create link to command_line binary in Debug mode", $verbose);
    }
}

sub runTest {
    # arguments:
    #    - mode: Release / Debug
    my ($mode) = @_;
    my $buildDirectory = $mode eq "Release" ? $releaseBuildDirectory : $debugBuildDirectory;
    my $testSubDirectory = platformIsLinux() ? "test" : "test/$mode";
    executeTestCommand("cd $buildDirectory; cd $testSubDirectory; ./skeleton_test", "run tests in $mode mode", $verbose);
}

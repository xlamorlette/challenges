package Test;

use lib '.';
use Build;
use Execute;
use Platform;

use File::Basename;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    runTest
);

sub runTest {
    # arguments:
    #    - mode: Release / Debug
    #    - verbose (optional)
    my ($mode) = @_;
    my $_verbose = $_[1] || 0;
    my $buildDirectory = getBuildDirectory($mode);
    my $commandHandler;
    if (platformIsLinux()) {
        my $command = "find $buildDirectory -executable -type f -name \"*test*\"";
        open $commandHandler, "$command 2>&1 |";
    } else {
        my $command = "Get-ChildItem -Path $buildDirectory -Recurse -Filter \"*test*.exe\" -Name";
        open $commandHandler, "powershell $command |";
    }
    while (<$commandHandler>) {
        my $executablePath = $_;
        chomp($executablePath);
        if (platformIsWindows()) {
            $executablePath = "$buildDirectory/$executablePath";
        }
        my $filename = basename($executablePath);
        executeTestCommand("./$executablePath", "run $filename tests in $mode mode", $_verbose);
    }
    close $commandHandler;
}

1;

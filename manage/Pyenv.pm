package Pyenv;

use lib '.';
use Execute;
use Platform;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    cleanPyenv
    configurePyenvUsage
    preparePyenv
);

sub cleanPyenv {
    # arguments:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm $pyenvDirectory", "clean Python virtualenv directory", $_verbose);
}

sub configurePyenvUsage {
    # arguments:
    #    - Python virtualenv directory location
    #    - verbose (optional)
    my ($location) = @_;
    my $_verbose = $_[1] || 0;
    my $_platform = platformIsLinux() ? "linux" : "windows";
    $pyenvDirectory = "$location/.pyenv-$_platform";
    print "Set Python virtualenv directory to ${commandColour}${pyenvDirectory}${normalText}\n" if ($_verbose);
    my $script = platformIsLinux() ? "bin/activate" : "Scripts/Activate.ps1";
    $pyenv = ". $pyenvDirectory/$script";
}

sub preparePyenv {
    # arguments:
    #    - requirements file
    #    - verbose (optional)
    my ($requirementsFile) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("python -m venv $pyenvDirectory", "initialise Python virtualenv", $_verbose);
    executeTestCommand("$pyenv; pip install -r $requirementsFile", "setup Python virtualenv", $_verbose);
    executeTestCommand("$pyenv; pip list --outdated", "list outdated dependencies", $_verbose);
}

1;

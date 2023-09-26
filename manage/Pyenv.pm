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
    local $verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm $pyenvDirectory", "clean Python virtualenv directory", $verbose);
}

sub configurePyenvUsage {
    # arguments:
    #    - Python virtualenv directory location
    #    - verbose (optional)
    my ($location) = @_;
    local $verbose = $_[1] || 0;
    # TODO: ternary
    if (platformIsWindows()) {
        $pyenvDirectory = "$location/.pyenv-windows";
    } else {
        $pyenvDirectory = "$location/.pyenv-linux";
    }
    print "Set Python virtualenv directory to ${commandColour}${pyenvDirectory}${normalText}\n" if (verbose);
    # TODO: ternary
    if (platformIsWindows()) {
        $pyenv = ". $pyenvDirectory/Scripts/Activate.ps1";
    } else {
        $pyenv = ". $pyenvDirectory/bin/activate";
    }
}

sub preparePyenv {
    # arguments:
    #    - requirements file
    #    - verbose (optional)
    my ($requirementsFile) = @_;
    local $verbose = $_[1] || 0;
    executeTestCommand("python -m venv $pyenvDirectory", "initialise Python virtualenv", $verbose);
    executeTestCommand("$pyenv; pip install -r $requirementsFile", "setup Python virtualenv", $verbose);
    executeTestCommand("$pyenv; pip list --outdated", "list outdated dependencies", $verbose);
}

1;

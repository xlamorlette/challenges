package Configure;

use lib '.';
use Platform;

use POSIX;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    configurePyenvUsage
    );

sub configurePyenvUsage {
    # arguments:
    #    - Python virtualenv directory location
    #    - verbose (optional)
    my ($location) = @_;
    local $verbose = $_[1] || 0;
    if (platformIsWindows()) {
        $pyenvDirectory = "$location/.pyenv-windows";
    } else {
        $pyenvDirectory = "$location/.pyenv-linux";
    }
    print "Set Python virtualenv directory to ${commandColour}${pyenvDirectory}${normalText}\n" if (verbose);
    if (platformIsWindows()) {
        $pyenv = ". $pyenvDirectory/Scripts/Activate.ps1";
    } else {
        $pyenv = ". $pyenvDirectory/bin/activate";
    }
}

1;

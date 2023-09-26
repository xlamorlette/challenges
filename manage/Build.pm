package Build;

use lib '.';
use Execute;
use Platform;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    build
);

sub build {
    # arguments:
    #    - mode: Release / Debug
    #    - verbose (optional)
    my ($mode) = @_;
    local $verbose = $_[1] || 0;
    my $buildDirectory = $mode eq "Release" ? $releaseBuildDirectory : $debugBuildDirectory;
    my $buildCommand = platformIsLinux()
        ? $ninja
        : "cmake --build . --config $mode";
    executeTestCommand("$pyenv; cd $buildDirectory; $buildCommand", "build in $mode mode", $verbose);
}

1;

package Prepare;

use lib '.';
use Configure;
use Execute;
use Platform;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    cleanBuild
    cleanMiscArtefacts
    cleanPyenv
    prepareBuild
    preparePyenv
    );

sub cleanBuild {
    # arguments:
    #    - verbose (optional)
    local $verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm ./$buildBaseDirectory", "clean build directory", $verbose);
}

sub cleanMiscArtefacts {
    # argument:
    #    - verbose (optional)
    local $verbose = $_[0] || 0;
    if (platformIsLinux()) {
        executeCommandIgnoreReturnCode("rm -rf .mypy_cache", "clean Mypy cache", $verbose);
        executeCommandIgnoreReturnCode("rm -rf test-reports 2>/dev/null", "clean test reports", $verbose);
        executeCommandIgnoreReturnCode("find . -name __pycache__ | xargs rm -rf", "clean Python caches", $verbose);
        executeCommandIgnoreReturnCode("find . -name *.egg-info | xargs rm -rf", "clean Python eggs", $verbose);
        executeCommandIgnoreReturnCode("find . -name .pytest_cache | xargs rm -rf", "clean Pytest cache", $verbose);
    }
}

sub cleanPyenv {
    # arguments:
    #    - verbose (optional)
    local $verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm $pyenvDirectory", "clean Python virtualenv directory", $verbose);
}

sub prepareBuild {
    # arguments:
    #    - baseDirectory
    #    - verbose (optional)
    my ($baseDirectory) = @_;
    local $verbose = $_[1] || 0;
    if (platformIsWindows()) {
        $cmakeExtraOptions .= " -DCMAKE_C_COMPILER=cl.exe -DCMAKE_CXX_COMPILER=cl.exe";
    }
    executeCommandIgnoreReturnCode("$mkdir $releaseBuildDirectory", "create Release build directory", $verbose);
    executeCommandIgnoreReturnCode("$mkdir $debugBuildDirectory", "create Debug build directory", $verbose);
    executeTestCommand("$pyenv; cd $releaseBuildDirectory; cmake -G Ninja -DCMAKE_BUILD_TYPE=Release "
        . "$cmakeExtraOptions $baseDirectory", "call cmake for Release", $verbose);
    executeTestCommand("$pyenv; cd $debugBuildDirectory; cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug "
        . "$cmakeExtraOptions $baseDirectory", "call cmake for Debug", $verbose);
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

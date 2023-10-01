package Build;

use lib '.';
use Execute;
use Platform;

use File::Basename;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    build
    cleanBuild
    cleanMiscArtefacts
    conanInstall
    getBuildDirectory
    runCMake
);

sub build {
    # arguments:
    #    - mode: Release / Debug
    #    - verbose (optional)
    my ($mode) = @_;
    my $_verbose = $_[1] || 0;
    my $buildDirectory = getBuildDirectory($mode);
    my $buildCommand = platformIsLinux()
        ? $ninja
        : "cmake --build . --config $mode";
    executeTestCommand("$pyenv; cd $buildDirectory; $buildCommand", "build in $mode mode", $_verbose);
    _linkExecutables("$mode", $_verbose);
}

sub _linkExecutables {
    # arguments:
    #    - mode: Release / Debug
    #    - verbose (optional)
    my ($mode) = @_;
    my $_verbose = $_[1] || 0;
    return if (! platformIsLinux());
    my $buildDirectory = getBuildDirectory($mode);
    my $command = "find $buildDirectory -executable -type f | grep -v CMake";
    my $commandHandler;
    open $commandHandler, "$command 2>&1 |";
    while (<$commandHandler>) {
        my $executablePath = $_;
        chomp($executablePath);
        my $filename = basename($executablePath);
        executeTestCommand("ln -sf $executablePath ${filename}_${mode}",
            "create link to filename binary in $mode mode", $_verbose);
    }
    close $commandHandler;
}

sub cleanBuild {
    # arguments:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm ./$buildBaseDirectory", "clean build directory", $_verbose);
}

sub cleanMiscArtefacts {
    # argument:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    if (platformIsLinux()) {
        executeCommandIgnoreReturnCode("$rm .mypy_cache", "clean Mypy cache", $_verbose);
        executeCommandIgnoreReturnCode("$rm test-reports 2>/dev/null", "clean test reports", $_verbose);
        executeCommandIgnoreReturnCode("find . -name __pycache__ | xargs rm -rf", "clean Python caches", $_verbose);
        executeCommandIgnoreReturnCode("find . -name *.egg-info | xargs rm -rf", "clean Python eggs", $_verbose);
        executeCommandIgnoreReturnCode("find . -name .pytest_cache | xargs rm -rf", "clean Pytest cache", $_verbose);
    } else {
        executeCommandIgnoreReturnCode("$rm CMakeUserPresets.json", "clean CMakeUserPresets", $_verbose);
    }
    _cleanLinks($_verbose);
}

sub _cleanLinks {
    # argument:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    return if (! platformIsLinux());
    executeCommandIgnoreReturnCode("find . -maxdepth 1 -type l | xargs rm -f", "remove links", $_verbose);
}

sub conanInstall {
    # arguments:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    executeTestCommand("$pyenv; conan profile detect --force", "detect Conan profile", $_verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Release --output-folder=$releaseBuildDirectory --build=missing",
        "install Conan packages in Release mode", $_verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Debug --output-folder=$debugBuildDirectory --build=missing",
        "install Conan packages in Debug mode", $_verbose);
}

sub getBuildDirectory {
    # arguments:
    #    - mode: Release / Debug
    my ($mode) = @_;
    return $mode eq "Release" ? $releaseBuildDirectory : $debugBuildDirectory;
}

sub runCMake {
    # arguments:
    #    - baseDirectory
    #    - verbose (optional)
    my ($baseDirectory) = @_;
    my $_verbose = $_[1] || 0;
    my $cmakeOptions = platformIsLinux()
        ? "-G Ninja"
        : "-DCMAKE_TOOLCHAIN_FILE='conan_toolchain.cmake'";
    executeTestCommand("$pyenv; cd $releaseBuildDirectory; "
        . "cmake $cmakeOptions -DCMAKE_BUILD_TYPE=Release $baseDirectory", "call CMake in Release mode", $_verbose);
    executeTestCommand("$pyenv; cd $debugBuildDirectory; "
        . "cmake $cmakeOptions -DCMAKE_BUILD_TYPE=Debug $baseDirectory", "call CMake in Debug mode", $_verbose);
}

1;
